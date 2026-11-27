"""Công cụ của bản chạy thử Adaptive Pre-class Scaffolding.

Mỗi công cụ là một hàm Python có @tool với docstring ghi đủ 4 ý:
    tên · input · output · có tác động ra ngoài không.
"""
import json
import os
import re

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_PATH = os.path.join(ROOT, "data", "lessons.json")

_QUIZ_PATTERNS = (
    "đáp án",
    "dap an",
    "chọn a",
    "chọn b",
    "chọn c",
    "chọn d",
    "câu nào đúng",
    "giải hộ quiz",
    "giải hộ bài kiểm tra",
    "làm hộ quiz",
    "làm giúp câu kiểm tra",
)

_OUT_OF_SCOPE_PATTERNS = (
    "tóm tắt cả bài",
    "tóm tắt toàn bộ",
    "sửa điểm",
    "chấm điểm",
    "đánh dấu hoàn thành",
    "viết code hộ toàn bộ",
    "ignore previous",
    "bỏ qua hướng dẫn",
)

_DISTRACTED_OR_NORMAL_PATTERNS = (
    "rời tab",
    "chuyển tab",
    "đi việc riêng",
    "đang đọc bình thường",
    "đọc bình thường",
    "đang ghi chép",
    "không kẹt",
)

_STUCK_PATTERNS = (
    "tua lại",
    "dừng lâu",
    "sai quiz",
    "làm sai",
    "kẹt",
    "khó hiểu",
    "chưa hiểu",
    "không hiểu",
    "quá tải",
    "giải thích",
    "là gì",
    "khác gì",
    "tại sao",
    "vì sao",
    "?",
)


def _load_lessons() -> list:
    if not os.path.exists(LESSONS_PATH):
        return []
    with open(LESSONS_PATH, encoding="utf-8") as f:
        return json.load(f)


@tool
def parse_learner_signal(text: str) -> dict:
    """Tên: parse_learner_signal — Phân tích tín hiệu hành vi và phạm vi yêu cầu của học viên.
    Input: chuỗi đầu vào text (str) gồm ngữ cảnh hành vi và/hoặc câu hỏi.
    Output: dict gồm segment_code, signal_type ('stuck' | 'distracted_or_normal'), is_quiz_answer_request, is_out_of_scope, query.
    Tác động ra ngoài: Không."""
    raw = (text or "").strip()
    lower = raw.lower()

    seg_match = re.search(r"\b(D\d{2}-S\d{2})\b", raw, flags=re.IGNORECASE)
    segment_code = seg_match.group(1).upper() if seg_match else ""

    is_quiz_answer_request = any(p in lower for p in _QUIZ_PATTERNS)
    is_out_of_scope = any(p in lower for p in _OUT_OF_SCOPE_PATTERNS)

    has_distracted = any(p in lower for p in _DISTRACTED_OR_NORMAL_PATTERNS)
    has_stuck = any(p in lower for p in _STUCK_PATTERNS)

    if has_distracted and not has_stuck and not is_quiz_answer_request and not is_out_of_scope:
        signal_type = "distracted_or_normal"
    else:
        signal_type = "stuck"

    return {
        "segment_code": segment_code,
        "signal_type": signal_type,
        "is_quiz_answer_request": is_quiz_answer_request,
        "is_out_of_scope": is_out_of_scope,
        "query": raw,
    }


@tool
def search_lesson(query: str, segment_code: str = "") -> list:
    """Tên: search_lesson — Tra cứu đoạn bài học AI20K trong data/lessons.json theo mã đoạn hoặc từ khoá.
    Input: query (str) và segment_code (str, tuỳ chọn).
    Output: danh sách tối đa 3 đoạn bài khớp {"code", "day", "topic", "title", "content", "common_trap"}.
    Tác động ra ngoài: Không."""
    lessons = _load_lessons()
    if not lessons:
        return []

    code_norm = (segment_code or "").strip().upper()
    if code_norm:
        exact = [item for item in lessons if item.get("code", "").upper() == code_norm]
        if exact:
            return [
                {
                    "code": item["code"],
                    "day": item["day"],
                    "topic": item["topic"],
                    "title": item["title"],
                    "content": item["content"],
                    "common_trap": item["common_trap"],
                }
                for item in exact[:1]
            ]

    q_lower = (query or "").lower()
    stopwords = {
        "bài", "ngoài", "học", "giải", "thích", "nào", "gì", "như", "với", "cho",
        "của", "và", "trong", "khi", "này", "đó", "là", "có", "không", "được",
        "làm", "cách", "một", "các", "những", "từ", "về", "ở", "nên", "thì",
        "đang", "vừa", "rồi", "mình", "bạn", "hãy", "xem", "đoạn", "phần",
    }
    tokens = [
        t for t in re.findall(r"[0-9a-zA-ZÀ-ỹ_-]+", q_lower)
        if len(t) >= 2 and t not in stopwords
    ]
    scored = []
    for item in lessons:
        score = 0
        for kw in item.get("keywords", []):
            if kw.lower() in q_lower:
                score += 3
        haystack = " ".join(
            [
                item.get("code", ""),
                item.get("day", ""),
                item.get("topic", ""),
                item.get("title", ""),
                item.get("content", ""),
            ]
        ).lower()
        haystack_tokens = set(re.findall(r"[0-9a-zA-ZÀ-ỹ_-]+", haystack))
        for tok in tokens:
            if tok in haystack_tokens:
                score += 1
        if score >= 3:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [
        {
            "code": item["code"],
            "day": item["day"],
            "topic": item["topic"],
            "title": item["title"],
            "content": item["content"],
            "common_trap": item["common_trap"],
        }
        for _, item in scored[:3]
    ]


@tool
def draft_scaffolding_card(segment_code: str, mode: str, body: str) -> dict:
    """Tên: draft_scaffolding_card — Tạo bản nháp thẻ gỡ kẹt bên lề để học viên tự xem hoặc gạt bỏ.
    Input: segment_code (str), mode (str), body (str).
    Output: dict {"status": "draft_for_learner", "segment_code", "mode", "card_text"}.
    Tác động ra ngoài: Không (chỉ tạo bản nháp hiển thị tại chỗ, không tự ghi điểm hay gửi tin)."""
    clean_body = (body or "").strip()
    if segment_code and segment_code not in clean_body:
        clean_body = "[%s] %s" % (segment_code, clean_body)
    card_text = (
        "[Thẻ gỡ kẹt · Mã đoạn: %s · Kiểu: %s]\n"
        "%s\n"
        "(Gợi ý bên lề — bạn có thể tự đối chiếu đoạn bài hoặc gạt bỏ nếu đã hiểu.)"
    ) % (segment_code or "N/A", mode or "Gợi ý", clean_body)
    return {
        "status": "draft_for_learner",
        "segment_code": segment_code,
        "mode": mode,
        "card_text": card_text,
    }
