"""Luồng chính của bản chạy thử Adaptive Pre-class Scaffolding (Workflow cố định 4 bước).

Khớp thiết kế tại spec.md §4:
1. parse_learner_signal(text) -> lọc yêu cầu xin đáp án/ngoài phạm vi và tín hiệu không kẹt
2. search_lesson(query, segment_code) -> tra căn cứ đoạn bài trong data/lessons.json
3. call_model(SYSTEM, user_prompt) -> chọn đúng 1 kiểu gỡ kẹt dựa trên căn cứ
4. draft_scaffolding_card(...) -> đóng gói thẻ nháp bên lề cho học viên tự quyết định
"""
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


def _extract_mode(text: str) -> str:
    for line in (text or "").splitlines():
        if line.strip().lower().startswith("kiểu:"):
            return line.split(":", 1)[1].strip() or "Gợi ý gỡ kẹt"
    return "Gợi ý gỡ kẹt"


def answer(text: str) -> dict:
    # Bước 1: Phân tích tín hiệu hành vi & lọc phạm vi an toàn
    sig = parse_learner_signal(text)

    if sig["is_quiz_answer_request"] or sig["is_out_of_scope"]:
        note("dừng: từ chối yêu cầu xin đáp án quiz hoặc ngoài phạm vi")
        hint = (" ở đoạn [%s]" % sig["segment_code"]) if sig["segment_code"] else ""
        return {
            "output": (
                "Mình không thể cung cấp đáp án quiz, tóm tắt cả bài hay thay đổi điểm/tiến độ. "
                "Bạn hãy xem lại khái niệm cốt lõi%s hoặc nói rõ ý bạn đang vướng để mình gợi ý cách tự suy luận nhé."
            ) % hint
        }

    if sig["signal_type"] == "distracted_or_normal":
        note("dừng: không xen vào (tín hiệu rời tab hoặc đang đọc bình thường)")
        return {
            "output": "[Không xen vào] Chưa phát hiện dấu hiệu kẹt kiến thức (rời tab hoặc đang đọc/ghi chép bình thường), giữ nguyên mạch học."
        }

    # Bước 2: Tra cứu đoạn bài học làm căn cứ
    found = search_lesson(sig["query"], sig["segment_code"])
    if not found:
        note("dừng: G10 thiếu căn cứ đoạn bài trong data/lessons.json")
        return {
            "output": (
                "Chưa có đoạn bài học khớp trong kho dữ liệu pre-class hiện tại nên mình không tự suy đoán ngoài tài liệu. "
                "Bạn vui lòng cung cấp mã đoạn (ví dụ D06-S01, D08-S01, D13-S01) hoặc nêu rõ tên khái niệm đang kẹt."
            )
        }

    # Bước 3: Gọi model chọn đúng 1 kiểu gỡ kẹt trên căn cứ đã tra
    top_code = found[0]["code"]
    context = "\n\n".join(
        "[%s | %s - %s]\nNội dung: %s\nBẫy thường gặp: %s"
        % (p["code"], p["day"], p["title"], p["content"], p["common_trap"])
        for p in found
    )
    user_prompt = (
        "Căn cứ đoạn bài:\n%s\n\n"
        "Tín hiệu / câu hỏi của học viên:\n%s"
    ) % (context, text)

    reply = call_model(SYSTEM, user_prompt)
    mode = _extract_mode(reply["text"])

    # Bước 4: Đóng gói thành thẻ gợi ý bản nháp bên lề
    card = draft_scaffolding_card(top_code, mode, reply["text"])
    return {"output": card["card_text"]}
