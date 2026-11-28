"""Luồng chính của bản chạy thử Adaptive Pre-class Scaffolding (Workflow cố định 4 bước).

Khớp thiết kế tại spec.md §4:
1. parse_learner_signal(text) -> lọc yêu cầu xin đáp án/ngoài phạm vi và tín hiệu không kẹt
2. search_lesson(query, segment_code) -> tra căn cứ đoạn bài trong data/lessons.json
3. call_model(SYSTEM, user_prompt) -> chọn đúng 1 kiểu gỡ kẹt dựa trên căn cứ
4. draft_scaffolding_card(...) -> đóng gói thẻ nháp bên lề cho học viên tự quyết định
"""
import re

from ai import call_model
from tools import draft_scaffolding_card, parse_learner_signal, search_lesson
from tracing import note

SYSTEM = """Bạn là trợ lý gỡ kẹt chủ động (Adaptive Pre-class Scaffolding) cho học viên AI20K khối L3.
Quy tắc bắt buộc:
1. CHỈ sử dụng thông tin có trong phần "Căn cứ đoạn bài" được cung cấp. Tuyệt đối KHÔNG bịa thêm kiến thức ngoài đoạn bài.
2. Chọn ĐÚNG 1 kiểu gỡ kẹt phù hợp nhất trong 3 kiểu sau:
   - Ẩn dụ đời thường (ví von ngắn gọn, dễ hình dung)
   - Sơ đồ Mermaid ngắn (tối đa 4-5 nút minh hoạ mối quan hệ)
   - 1 câu hỏi gợi mở (giúp học viên tự nghĩ ra ý cốt lõi)
3. Luôn trích rõ mã đoạn bài dạng [DXX-SYY] trong phần trả lời.
4. Tuyệt đối KHÔNG nêu đáp án đúng/sai của câu kiểm tra (quiz), KHÔNG tóm tắt cả bài.
5. Trả lời ngắn gọn dưới 120 từ theo đúng mẫu:
Kiểu: <tên 1 trong 3 kiểu>
<nội dung gỡ kẹt kèm mã [DXX-SYY]>"""

MAX_STEPS = 4


_ANSWER_LEAK_RE = re.compile(
    r"(đáp án(\s+đúng)?\s*(là|:)|chọn\s+(phương án|đáp án)?\s*[ABCD]\b|"
    r"câu trả lời(\s+đúng)?\s*(là|:)\s*[ABCD]\b|"
    r"(correct\s+)?answer\s+is\s*[ABCD]\b)",
    flags=re.IGNORECASE,
)


def _extract_mode(text: str) -> str:
    for line in (text or "").splitlines():
        if line.strip().lower().startswith("kiểu:"):
            return line.split(":", 1)[1].strip() or "Gợi ý gỡ kẹt"
    return "Gợi ý gỡ kẹt"


def _apply_output_guardrail(text: str, valid_codes: list, fallback_code: str) -> str:
    """Chốt chặn 4 — Hậu kiểm đầu ra AI:
    - Chặn mẫu rò rỉ đáp án quiz (tiếng Việt & tiếng Anh)
    - Sửa mã đoạn lạ không có trong căn cứ hoặc bổ sung mã đoạn nếu thiếu
    - Giới hạn độ dài <= 140 từ tránh quá tải nhận thức
    """
    out = (text or "").strip()
    if _ANSWER_LEAK_RE.search(out):
        note("guardrail: chặn mẫu rò rỉ đáp án trong output model")
        return (
            "Kiểu: 1 câu hỏi gợi mở\n"
            "Mình không nêu đáp án trực tiếp — bạn hãy đối chiếu lại ý cốt lõi ở đoạn [%s] và tự kiểm tra lại lựa chọn nhé."
        ) % fallback_code

    valid_set = {c.upper() for c in valid_codes}
    has_valid_code = False
    for m in re.finditer(r"\b(D\d{2}-S\d{2})\b", out, flags=re.IGNORECASE):
        code = m.group(1).upper()
        if code not in valid_set:
            note("guardrail: thay mã đoạn ngoài căn cứ %s -> %s" % (code, fallback_code))
            out = out.replace(m.group(1), fallback_code)
        else:
            has_valid_code = True

    if not has_valid_code and fallback_code:
        out = "%s [%s]" % (out, fallback_code)

    words = out.split()
    if len(words) > 140:
        out = " ".join(words[:140]).rstrip(",;:") + "…"
    return out


def answer(text: str) -> dict:
    # Chốt chặn 1 (Input Gate): Chặn input rỗng, tấn công/vượt quyền và tín hiệu không kẹt trước khi gọi model
    if not (text or "").strip():
        note("chốt chặn 1: input rỗng -> G10")
        return {"output": "Chưa nhận được nội dung câu hỏi hoặc tín hiệu học tập."}

    sig = parse_learner_signal(text)

    if sig["is_attack"] or ((sig["is_quiz_answer_request"] or sig["is_out_of_scope"]) and not sig["is_soft_shortcut"]):
        note("chốt chặn 1: từ chối yêu cầu tấn công / vượt thẩm quyền")
        hint = (" ở đoạn [%s]" % sig["segment_code"]) if sig["segment_code"] else ""
        return {
            "output": (
                "Mình không thể cung cấp đáp án quiz, sửa điểm hay thực hiện thao tác ngoài phạm vi hỗ trợ học tập. "
                "Bạn hãy xem lại khái niệm cốt lõi%s hoặc liên hệ TA nếu gặp lỗi hệ thống nhé."
            ) % hint
        }

    if sig["is_soft_shortcut"]:
        note("chốt chặn 1: chặn lối tắt, từ chối giải hộ/tóm tắt cả bài, giữ gợi mở đúng đoạn")
        found_hint = search_lesson(sig["query"], sig["segment_code"])
        if found_hint:
            seg = found_hint[0]
            first_sentence = seg["content"].split(".")[0].strip()
            return {
                "output": (
                    "Mình không thể cho đáp án quiz hay tóm tắt toàn bộ bài giúp bạn. "
                    "Thu hẹp về đúng đoạn [%s — %s]: %s. Bạn thử đối chiếu ý này để tự trả lời tiếp nhé!"
                ) % (seg["code"], seg["title"], first_sentence)
            }
        return {
            "output": (
                "Mình không thể cung cấp đáp án quiz hay tóm tắt toàn bộ bài. "
                "Bạn hãy cho biết cụ thể mã đoạn đang vướng (vd D06-S01, D12-S01) để mình gợi mở đúng ý cốt lõi nhé."
            )
        }

    if sig["signal_type"] == "distracted_or_normal":
        note("chốt chặn 1: không xen vào (tín hiệu rời tab hoặc đang đọc bình thường)")
        return {
            "output": "[Không xen vào] Chưa phát hiện dấu hiệu kẹt kiến thức (rời tab hoặc đang đọc/ghi chép bình thường), giữ nguyên mạch học."
        }

    # Chốt chặn 2 (Grounding + G10): Tra căn cứ bài học; thiếu căn cứ thì dừng, tuyệt đối không bịa
    found = search_lesson(sig["query"], sig["segment_code"])
    if not found:
        note("chốt chặn 2: G10 thiếu căn cứ đoạn bài trong data/lessons.json")
        return {
            "output": (
                "Chưa có đoạn bài học khớp trong kho dữ liệu pre-class hiện tại nên mình không tự suy đoán ngoài tài liệu. "
                "Bạn vui lòng cung cấp mã đoạn (ví dụ D06-S01, D08-S01, D13-S01) hoặc nêu rõ tên khái niệm đang kẹt."
            )
        }

    # Chốt chặn 3 (Bounded Execution): Workflow cố định, tối đa 1 lần gọi model cho mỗi lượt
    model_budget = 1
    top_code = found[0]["code"]
    valid_codes = [p["code"] for p in found]
    context = "\n\n".join(
        "[%s | %s - %s]\nNội dung: %s\nBẫy thường gặp: %s"
        % (p["code"], p["day"], p["title"], p["content"], p["common_trap"])
        for p in found
    )
    user_prompt = (
        "Căn cứ đoạn bài:\n%s\n\n"
        "Tín hiệu / câu hỏi của học viên:\n%s"
    ) % (context, text)

    if model_budget <= 0:
        raise RuntimeError("Vượt quá ngân sách gọi model cho 1 lượt")
    model_budget -= 1
    reply = call_model(SYSTEM, user_prompt)

    # Chốt chặn 4 (Output Guardrail): Hậu kiểm chống lộ đáp án, mã đoạn bịa và độ dài
    safe_text = _apply_output_guardrail(reply["text"], valid_codes, top_code)
    mode = _extract_mode(safe_text)

    # Chốt chặn 5 (Human-in-the-loop): Chỉ tạo bản nháp thẻ gợi ý bên lề, không tác động ra ngoài
    card = draft_scaffolding_card(top_code, mode, safe_text)
    return {"output": card["card_text"]}
