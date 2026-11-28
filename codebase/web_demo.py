"""Giao diện Web Demo cục bộ kiểu Preclass Online cho HoiClaude — Adaptive Pre-class Scaffolding.

Trải nghiệm tối giản cho người học thật (không số liệu kỹ thuật gây rối):
- Đọc bài giảng & xem thanh tiến độ video ngay trên màn hình chính.
- Tự động cảm nhận hành vi thật trên trình duyệt:
  + Bấm "Tua lại 15s" từ 2 lần trở lên -> trợ lý tự bật 1 thẻ gỡ kẹt ngắn gọn bên lề.
  + Chọn sai câu hỏi kiểm tra giữa bài -> trợ lý tự gợi mở (0% lộ đáp án).
  + Rời sang tab khác rồi quay lại / đọc bình thường -> trợ lý giữ im lặng, không nhảy pop-up.
- Hỏi đáp trực tiếp ở ô chat bên phải (tự tìm đúng đoạn bài trong `data/lessons.json` hoặc báo thiếu căn cứ G10).
- Nút "Trace" nhỏ ở góc trên phải (ẩn mặc định) dành riêng cho giám khảo khi cần xem token thật & log `tracing.py`.

Chỉ dùng thư viện chuẩn của Python (http.server). Gọi trực tiếp `codebase/agent.py -> answer()`.
"""
import argparse
import json
import os
import re
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CODEBASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CODEBASE_DIR)
LESSONS_PATH = os.path.join(ROOT_DIR, "data", "lessons.json")

if CODEBASE_DIR not in sys.path:
    sys.path.insert(0, CODEBASE_DIR)

import tracing  # noqa: E402
from agent import answer  # noqa: E402

_TRACE_LOCK = threading.Lock()

# Câu hỏi kiểm tra nhanh bám đúng nội dung 12 đoạn trong data/lessons.json
# (chỉ dùng phía trình duyệt để học viên tự thử bấm đúng/sai; đáp án KHÔNG gửi vào prompt AI)
MINI_QUIZZES = {
    "D08-S01": {
        "question": "Khi cắt đoạn tài liệu (chunking) cho RAG, rủi ro chính nếu cắt quá nhỏ là gì?",
        "options": [
            "Mất ngữ cảnh câu trước–sau nên AI khó hiểu đúng ý đoạn văn",
            "Tăng kích thước file gốc lên gấp đôi",
            "Bắt buộc phải đổi sang mô hình lớn nhất",
        ],
        "correct": 0,
    },
    "D08-S02": {
        "question": "Theo nguyên tắc G10 (Abstention), khi công cụ tra cứu không tìm thấy đoạn bài phù hợp, trợ lý nên làm gì?",
        "options": [
            "Tự trả lời dựa trên kiến thức tổng quát cho mượt",
            "Nói rõ chưa có đủ căn cứ trong bài học thay vì tự suy đoán",
            "Chọn ngẫu nhiên một đoạn bất kỳ để gắn mã nguồn",
        ],
        "correct": 1,
    },
    "D06-S01": {
        "question": "Vì sao cần chốt chuẩn \"đạt\" (threshold) trước khi chạy đánh giá?",
        "options": [
            "Để tiết kiệm số lượng token khi gọi API",
            "Để tránh tự sửa tiêu chí cho khớp với kết quả sau khi chạy",
            "Để không cần viết bộ câu thử khó",
        ],
        "correct": 1,
    },
    "D06-S02": {
        "question": "Với trợ lý học tập chủ động, vì sao nên ưu tiên Precision cao ở ngưỡng can thiệp?",
        "options": [
            "Để trợ lý bật gợi ý liên tục mỗi khi học viên dừng chuột",
            "Để hạn chế báo nhầm gây phiền và đứt mạch tập trung khi học viên đang đọc bình thường",
            "Để tăng tốc độ tải trang web",
        ],
        "correct": 1,
    },
    "D12-S01": {
        "question": "Chi phí thực tế của một hệ thống AI cần tính theo chỉ số nào?",
        "options": [
            "Chỉ tính số token đầu vào của 1 câu ngắn nhất",
            "Chi phí trên mỗi task thành công (tính cả các lượt lỗi / gọi lặp và giá token ra đắt hơn token vào)",
            "Giá gói miễn phí lúc đang phát triển",
        ],
        "correct": 1,
    },
    "D13-S01": {
        "question": "Mục tiêu của Scaffolding vừa đủ khi học viên bị quá tải nhận thức là gì?",
        "options": [
            "Đổ ra bài giải thích dài 500 chữ thay cho toàn bộ slide",
            "Đưa đúng 1 điểm tựa ngắn gọn (ẩn dụ / sơ đồ / câu hỏi gợi mở) rồi để học viên tự bước tiếp",
            "Tự động bấm hoàn thành bài học hộ học viên",
        ],
        "correct": 1,
    },
    "D13-S02": {
        "question": "Vì sao trợ lý không nên đưa trực tiếp đáp án quiz hay tóm tắt hộ trọn bài?",
        "options": [
            "Vì làm người học ỷ lại (Cognitive Offloading), không tự hình thành hiểu biết thật",
            "Vì mô hình không thể đọc được chữ tiếng Việt",
            "Vì trình duyệt chặn hiển thị đáp án",
        ],
        "correct": 0,
    },
    "D13-S03": {
        "question": "Khi học viên chỉ rời tab đi việc riêng hoặc dừng đọc/ghi chép bình thường, hệ thống nên làm gì?",
        "options": [
            "Bật ngay pop-up lớn giữa màn hình hỏi thăm",
            "Giữ im lặng, không xen vào để bảo vệ mạch tập trung",
            "Tự động tóm tắt lại cả bài học",
        ],
        "correct": 1,
    },
}


def load_lessons():
    if not os.path.exists(LESSONS_PATH):
        return []
    with open(LESSONS_PATH, encoding="utf-8") as f:
        items = json.load(f)
    for item in items:
        item["quiz"] = MINI_QUIZZES.get(item["code"])
    return items


def classify_output(output_text: str) -> dict:
    text = (output_text or "").strip()
    codes = sorted(set(re.findall(r"\bD\d{2}-S\d{2}\b", text.upper())))
    if text.startswith("[Không xen vào]"):
        return {"kind": "silent", "label": "Giữ im lặng", "codes": codes}
    if text.startswith("Mình không thể cung cấp đáp án"):
        return {"kind": "refuse", "label": "Không lộ đáp án", "codes": codes}
    if text.startswith("Chưa có đoạn bài học khớp"):
        return {"kind": "abstain", "label": "Ngoài tài liệu bài học", "codes": codes}
    return {"kind": "card", "label": "Gợi ý gỡ kẹt", "codes": codes}


def run_agent_traced(input_text: str) -> dict:
    with _TRACE_LOCK:
        t0 = time.perf_counter()
        tracing.begin("web_demo")
        error = None
        output = ""
        try:
            res = answer(input_text)
            output = res.get("output", "") if isinstance(res, dict) else str(res)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        summary, events = tracing.end()
        latency_s = round(time.perf_counter() - t0, 3)

    return {
        "input": input_text,
        "output": output,
        "error": error,
        "meta": classify_output(output),
        "summary": summary,
        "latency_s": latency_s,
        "events": events,
    }


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Preclass Online</title>
  <style>
    :root {
      --navy: #0a4968;
      --navy-dark: #073851;
      --navy-soft: #eef6fa;
      --orange: #c95221;
      --ink: #0f2937;
      --muted: #64748b;
      --line: #e2e8f0;
      --bg: #ffffff;
      --surface: #f8fafc;
    }
    * { box-sizing: border-box; }
    html, body { height: 100%; margin: 0; }
    body {
      font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      background: var(--bg);
      color: var(--ink);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* TOP NAVBAR */
    .topbar {
      height: 52px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      padding: 0 18px;
      display: flex; align-items: center; justify-content: space-between;
      flex-shrink: 0;
    }
    .topbar-left { display: flex; align-items: center; gap: 12px; }
    .icon-btn {
      width: 34px; height: 34px; border: none; background: transparent;
      border-radius: 8px; cursor: pointer; font-size: 18px; color: var(--ink);
      display: grid; place-items: center;
    }
    .icon-btn:hover { background: var(--surface); }
    .brand { font-size: 16px; }
    .brand strong { color: var(--navy-dark); font-weight: 800; }
    .brand span { color: var(--muted); font-weight: 400; margin-left: 2px; }

    .topbar-right { display: flex; align-items: center; gap: 10px; }
    .trace-toggle {
      border: 1px solid var(--line); background: #ffffff; color: var(--muted);
      border-radius: 999px; padding: 5px 11px; font-size: 11.5px; font-weight: 600;
      cursor: pointer;
    }
    .trace-toggle:hover { border-color: var(--navy); color: var(--navy); }
    .user-pill {
      display: inline-flex; align-items: center; gap: 7px;
      border: 1px solid var(--line); border-radius: 999px;
      padding: 3px 11px 3px 4px; font-size: 12px; font-weight: 600;
    }
    .avatar {
      width: 24px; height: 24px; border-radius: 50%;
      background: var(--navy); color: #ffffff;
      font-size: 10.5px; font-weight: 700; display: grid; place-items: center;
    }

    /* BLUE BANNER — giống hệt Preclass Online */
    .subbar {
      height: 46px;
      background: linear-gradient(90deg, #063d58 0%, #0a5275 100%);
      border-bottom: 2px solid var(--orange);
      color: #ffffff;
      padding: 0 22px;
      display: flex; align-items: center; justify-content: space-between;
      flex-shrink: 0;
    }
    .subbar-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
    .subbar-badge {
      font-size: 10px; font-weight: 700; letter-spacing: 0.06em;
      color: #bae6fd; text-transform: uppercase;
    }
    .subbar-title { font-size: 13px; font-weight: 700; color: #ffffff; }
    .subbar-status {
      font-size: 11.5px; color: #dcfce7;
      background: rgba(255,255,255,0.12);
      padding: 4px 12px; border-radius: 999px;
      display: inline-flex; align-items: center; gap: 6px;
    }
    .dot { width: 7px; height: 7px; border-radius: 50%; background: #34d399; }

    /* MAIN 2-COLUMN LAYOUT */
    .workspace {
      flex: 1; min-height: 0;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
    }
    @media (max-width: 900px) {
      body { overflow: auto; }
      .workspace { grid-template-columns: 1fr; }
    }

    /* LEFT DRAWER (Mục lục bài học) */
    .backdrop { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.25); z-index: 40; }
    .drawer {
      position: fixed; top: 0; left: 0; bottom: 0; width: 295px; max-width: 85vw;
      background: #ffffff; border-right: 1px solid var(--line);
      box-shadow: 10px 0 30px rgba(15, 23, 42, 0.14);
      z-index: 50; display: flex; flex-direction: column;
    }
    .drawer-head {
      height: 52px; padding: 0 16px; border-bottom: 1px solid var(--line);
      display: flex; align-items: center; justify-content: space-between;
      font-weight: 700; font-size: 14px; color: var(--navy-dark);
    }
    .drawer-list { flex: 1; overflow-y: auto; padding: 8px 0 20px; }
    .day-hdr {
      padding: 10px 16px 4px; display: flex; gap: 10px;
      font-size: 12.5px; font-weight: 700; color: var(--navy-dark);
    }
    .day-hdr .d-num { color: var(--orange); width: 28px; flex-shrink: 0; }
    .seg-btn {
      width: 100%; border: none; background: transparent;
      padding: 8px 16px 8px 22px; text-align: left; cursor: pointer;
      display: flex; align-items: flex-start; gap: 10px;
      border-left: 3px solid transparent;
    }
    .seg-btn:hover { background: var(--surface); }
    .seg-btn.active { background: var(--navy-soft); border-left-color: var(--navy); }
    .seg-dot {
      width: 13px; height: 13px; border-radius: 50%;
      border: 1.5px solid #cbd5e1; margin-top: 3px; flex-shrink: 0;
    }
    .seg-btn.active .seg-dot { border-color: var(--navy); background: var(--navy); box-shadow: inset 0 0 0 3px #fff; }
    .seg-t { font-size: 12.5px; font-weight: 600; color: var(--ink); line-height: 1.35; }
    .seg-c { font-size: 11px; color: var(--muted); }

    /* CENTER LESSON COLUMN */
    .lesson-col {
      padding: 18px 28px 24px;
      overflow-y: auto;
      display: flex; flex-direction: column; gap: 16px;
    }
    .lesson-head {
      display: flex; align-items: center; justify-content: space-between; gap: 12px;
    }
    .lesson-head h1 { margin: 0; font-size: 21px; font-weight: 800; color: var(--navy-dark); }
    .next-btn {
      background: var(--navy); color: #ffffff; border: none;
      border-radius: 9px; padding: 8px 14px; font-size: 12.5px; font-weight: 700;
      cursor: pointer; flex-shrink: 0;
    }
    .next-btn:hover { background: var(--navy-dark); }

    /* SLIDE PLAYER CARD */
    .player-card {
      background: #f8fbfd;
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
      transition: box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .player-card.highlight {
      border: 2px solid #0d9488;
      box-shadow: 0 0 0 5px rgba(13, 148, 136, 0.14);
    }
    .slide-body {
      padding: 26px 30px 24px;
      background: linear-gradient(180deg, #ffffff 0%, #f8fbfd 100%);
    }
    .slide-tag {
      display: inline-block; font-size: 11px; font-weight: 700;
      color: var(--navy); background: var(--navy-soft);
      padding: 3px 9px; border-radius: 6px; margin-bottom: 12px;
    }
    .slide-title { margin: 0 0 14px; font-size: 22px; font-weight: 800; color: var(--navy-dark); line-height: 1.3; }
    .slide-text { margin: 0; font-size: 15.5px; line-height: 1.8; color: #1e293b; }

    /* REAL SIMPLE PLAYER BAR */
    .player-controls {
      background: #0f2937; color: #f8fafc;
      padding: 10px 18px;
      display: flex; align-items: center; gap: 12px;
    }
    .ctrl-btn {
      border: none; background: rgba(255,255,255,0.12); color: #ffffff;
      border-radius: 8px; padding: 6px 12px; font-size: 12.5px; font-weight: 600;
      cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
      flex-shrink: 0;
    }
    .ctrl-btn:hover { background: rgba(255,255,255,0.22); }
    .ctrl-btn.rewind-hot { background: #0d9488; }
    .progress-wrap {
      flex: 1; height: 6px; background: rgba(255,255,255,0.2);
      border-radius: 999px; overflow: hidden; cursor: pointer;
    }
    .progress-fill { height: 100%; width: 42%; background: #38bdf8; transition: width 0.25s ease; }
    .time-label { font-size: 11.5px; color: #cbd5e1; font-variant-numeric: tabular-nums; flex-shrink: 0; }

    /* MINI QUIZ RIGHT BELOW SLIDE */
    .quiz-card {
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 18px 22px;
    }
    .quiz-kicker { font-size: 11px; font-weight: 700; color: var(--orange); text-transform: uppercase; letter-spacing: 0.06em; }
    .quiz-q { margin: 6px 0 12px; font-size: 15px; font-weight: 700; color: var(--ink); }
    .quiz-opts { display: flex; flex-direction: column; gap: 8px; }
    .quiz-opt {
      width: 100%; text-align: left;
      border: 1px solid var(--line); background: #ffffff;
      border-radius: 10px; padding: 10px 14px;
      font-size: 13.5px; color: var(--ink); cursor: pointer;
      transition: all 0.15s ease;
    }
    .quiz-opt:hover { border-color: var(--navy); background: var(--navy-soft); }
    .quiz-opt.correct { border-color: #10b981; background: #ecfdf5; color: #065f46; font-weight: 600; }
    .quiz-opt.wrong { border-color: #ef4444; background: #fef2f2; color: #991b1b; }
    .quiz-feedback { margin-top: 10px; font-size: 13px; font-weight: 600; }
    .quiz-feedback.ok { color: #059669; }
    .quiz-feedback.err { color: #dc2626; }

    /* RIGHT SIDE PANEL — TƯƠNG TÁC LỚP HỌC (sạch hoàn toàn!) */
    .side-col {
      border-left: 1px solid var(--line);
      background: #ffffff;
      display: flex; flex-direction: column; min-height: 0;
    }
    .side-head {
      padding: 14px 16px 12px;
      border-bottom: 1px solid #f1f5f9;
    }
    .side-head h2 { margin: 0; font-size: 14.5px; font-weight: 800; color: var(--ink); }
    .side-head p { margin: 3px 0 0; font-size: 12px; color: var(--muted); }

    .feed {
      flex: 1; overflow-y: auto;
      padding: 16px;
      display: flex; flex-direction: column; gap: 12px;
    }
    .calm-empty {
      margin: auto 0; text-align: center; padding: 20px 12px;
      color: var(--muted); font-size: 13px; line-height: 1.6;
    }
    .calm-empty strong { display: block; color: var(--ink); font-size: 14px; margin-bottom: 6px; }
    .calm-tips {
      margin-top: 14px; text-align: left;
      background: var(--surface); border: 1px solid var(--line);
      border-radius: 12px; padding: 12px 14px; font-size: 12.5px;
    }
    .calm-tips ul { margin: 6px 0 0; padding-left: 18px; }
    .calm-tips li { margin-bottom: 4px; }

    .user-msg {
      align-self: flex-end; max-width: 88%;
      background: var(--navy-soft); color: var(--navy-dark);
      border-radius: 14px 14px 4px 14px;
      padding: 9px 13px; font-size: 13px; line-height: 1.5;
    }
    .quiet-note {
      align-self: center; font-size: 11.5px; color: var(--muted);
      background: var(--surface); border: 1px solid var(--line);
      border-radius: 999px; padding: 5px 12px;
    }
    .ai-card {
      background: #ffffff;
      border: 1px solid var(--line);
      border-left: 4px solid #0d9488;
      border-radius: 12px;
      padding: 13px 14px;
      box-shadow: 0 3px 12px rgba(15, 41, 55, 0.06);
    }
    .ai-card.kind-abstain { border-left-color: #d97706; background: #fffbeb; }
    .ai-card.kind-refuse { border-left-color: #dc2626; background: #fef2f2; }
    .ai-card-top {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;
    }
    .ai-label { font-size: 11.5px; font-weight: 700; color: #0f766e; }
    .kind-abstain .ai-label { color: #92400e; }
    .kind-refuse .ai-label { color: #991b1b; }
    .dismiss-btn {
      border: none; background: transparent; color: var(--muted);
      font-size: 12px; cursor: pointer; padding: 2px 6px; border-radius: 6px;
    }
    .dismiss-btn:hover { background: rgba(15, 23, 42, 0.06); color: var(--ink); }
    .ai-text { white-space: pre-wrap; font-size: 13.5px; line-height: 1.65; color: var(--ink); }
    .ai-actions { margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }
    .cite-chip {
      border: 1px solid #cce3ef; background: var(--navy-soft); color: var(--navy);
      border-radius: 7px; padding: 4px 10px; font-size: 11.5px; font-weight: 700;
      cursor: pointer;
    }
    .cite-chip:hover { background: var(--navy); color: #ffffff; }

    /* CHAT INPUT AT BOTTOM */
    .chat-box {
      padding: 10px 14px 12px;
      border-top: 1px solid var(--line);
      background: #ffffff;
    }
    .chat-form {
      display: flex; align-items: center; gap: 8px;
      border: 1px solid #cbd5e1; border-radius: 12px;
      padding: 5px 6px 5px 12px;
    }
    .chat-form:focus-within { border-color: var(--navy); box-shadow: 0 0 0 3px rgba(10, 73, 104, 0.1); }
    .chat-form input {
      flex: 1; border: none; outline: none; font-size: 13px; font-family: inherit;
    }
    .send-btn {
      width: 34px; height: 34px; border: none; border-radius: 9px;
      background: var(--navy); color: #ffffff; font-size: 15px; cursor: pointer;
      display: grid; place-items: center; flex-shrink: 0;
    }
    .send-btn:hover { background: var(--navy-dark); }
    .send-btn:disabled { opacity: 0.5; cursor: wait; }
    .chat-hint { margin-top: 6px; font-size: 10.5px; color: var(--muted); }

    /* HIDDEN JUDGE TRACE MODAL (chỉ mở khi bấm nút "Trace" góc trên phải) */
    .modal-panel {
      position: fixed; top: 52px; right: 0; bottom: 0; width: 420px; max-width: 92vw;
      background: #0b191c; color: #e2e8f0; z-index: 60;
      border-left: 1px solid #1e3a40; box-shadow: -10px 0 30px rgba(0,0,0,0.25);
      display: flex; flex-direction: column;
    }
    .modal-head {
      padding: 14px 16px; border-bottom: 1px solid #1e3a40;
      display: flex; justify-content: space-between; align-items: center;
      font-size: 13px; font-weight: 700; color: #5eead4;
    }
    .modal-body { flex: 1; overflow-y: auto; padding: 14px 16px; display: flex; flex-direction: column; gap: 12px; }
    .modal-close { border: none; background: transparent; color: #94a3b8; font-size: 18px; cursor: pointer; }
    .trace-meta { font-family: Consolas, monospace; font-size: 12px; color: #99f6e4; background: #102429; padding: 10px; border-radius: 8px; }
    .trace-ev { font-family: Consolas, monospace; font-size: 11px; background: #132c32; padding: 8px 10px; border-radius: 8px; word-break: break-word; }
    .judge-box textarea {
      width: 100%; background: #102429; color: #f0fdfa; border: 1px solid #24464e;
      border-radius: 8px; padding: 8px; font-size: 12px; font-family: inherit; min-height: 68px;
    }
    .judge-box button {
      margin-top: 6px; width: 100%; background: #14b8a6; color: #042f2e;
      border: none; border-radius: 8px; padding: 8px; font-weight: 700; cursor: pointer;
    }
    .hidden { display: none !important; }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-left">
      <button type="button" class="icon-btn" id="openDrawerBtn" title="Mục lục bài học">☰</button>
      <div class="brand"><strong>Preclass</strong><span>Online</span></div>
    </div>
    <div class="topbar-right">
      <button type="button" class="trace-toggle" id="openTraceBtn" title="Mở nhật ký kỹ thuật cho giám khảo">Trace</button>
      <span class="user-pill"><span class="avatar">L3</span> Học viên L3</span>
    </div>
  </header>

  <div class="subbar">
    <div class="subbar-left">
      <div>
        <div class="subbar-badge">BÀI HỌC PRE-CLASS</div>
        <div class="subbar-title" id="bannerTitle">Đang tải...</div>
      </div>
    </div>
    <span class="subbar-status"><span class="dot"></span> Trợ lý chỉ hỗ trợ khi bạn kẹt</span>
  </div>

  <!-- DRAWER MỤC LỤC -->
  <div class="backdrop hidden" id="backdrop"></div>
  <nav class="drawer hidden" id="drawer">
    <div class="drawer-head">
      <span>Mục lục bài học</span>
      <button type="button" class="icon-btn" id="closeDrawerBtn">✕</button>
    </div>
    <div class="drawer-list" id="drawerList"></div>
  </nav>

  <!-- MODAL TRACE ẨN DÀNH CHO GIÁM KHẢO -->
  <aside class="modal-panel hidden" id="traceModal">
    <div class="modal-head">
      <span>Trace &amp; Câu thử giám khảo</span>
      <button type="button" class="modal-close" id="closeTraceBtn">✕</button>
    </div>
    <div class="modal-body">
      <div class="trace-meta" id="traceSummary">Chưa có lượt gọi nào.</div>
      <div class="judge-box">
        <div style="font-size:11px; color:#94a3b8; margin-bottom:5px;">Dán trực tiếp 1 câu thử lạ gửi vào <code>agent.answer()</code>:</div>
        <textarea id="judgeInput" placeholder="Ví dụ: Bài: Day 06 | Hành vi: dừng 180s, chuyển sang tab khác..."></textarea>
        <button type="button" id="judgeRunBtn">Chạy câu thử</button>
      </div>
      <div id="traceList" style="display:flex; flex-direction:column; gap:8px;"></div>
    </div>
  </aside>

  <!-- WORKSPACE 2 CỘT SẠCH SẼ -->
  <main class="workspace">
    <!-- BÊN TRÁI: BÀI HỌC + PLAYER + QUIZ THẬT -->
    <section class="lesson-col">
      <div class="lesson-head">
        <h1 id="topicTitle">RAG &amp; Grounding</h1>
        <button type="button" class="next-btn" id="nextBtn">Chuyển phần tiếp theo ›</button>
      </div>

      <article class="player-card" id="playerCard">
        <div class="slide-body">
          <span class="slide-tag" id="slideTag">Day 08 · Mã đoạn D08-S01</span>
          <h2 class="slide-title" id="slideTitle">...</h2>
          <p class="slide-text" id="slideText">...</p>
        </div>

        <div class="player-controls">
          <button type="button" class="ctrl-btn" id="playBtn">▶ Tiếp tục học</button>
          <button type="button" class="ctrl-btn" id="rewindBtn" title="Bấm tua lại 2 lần nếu đoạn này khó hiểu">↺ Tua lại 15s</button>
          <div class="progress-wrap" id="progressBar"><div class="progress-fill" id="progressFill"></div></div>
          <span class="time-label" id="timeLabel">02:15 / 05:20</span>
        </div>
      </article>

      <section class="quiz-card hidden" id="quizCard">
        <div class="quiz-kicker">Câu hỏi kiểm tra nhanh</div>
        <div class="quiz-q" id="quizQuestion"></div>
        <div class="quiz-opts" id="quizOpts"></div>
        <div class="quiz-feedback" id="quizFeedback"></div>
      </section>
    </section>

    <!-- BÊN PHẢI: TƯƠNG TÁC LỚP HỌC -->
    <aside class="side-col">
      <div class="side-head">
        <h2>Tương tác lớp học</h2>
        <p>Thẻ gỡ kẹt hiện gọn bên lề, không che bài học.</p>
      </div>

      <div class="feed" id="feed">
        <div class="calm-empty" id="calmEmpty">
          <strong>Mạch học đang yên tĩnh</strong>
          Trợ lý sẽ không tự nhảy pop-up làm phiền khi bạn đọc bình thường hoặc chuyển tab.
          <div class="calm-tips">
            <strong>Thử trải nghiệm tự nhiên:</strong>
            <ul>
              <li>Bấm <strong>↺ Tua lại 15s</strong> 2 lần nếu thấy đoạn bài khó hiểu.</li>
              <li>Thử làm câu kiểm tra nhanh bên dưới bài học.</li>
              <li>Chuyển sang tab trình duyệt khác rồi quay lại — trợ lý vẫn giữ im lặng.</li>
              <li>Hoặc gõ câu hỏi trực tiếp vào ô bên dưới.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="chat-box">
        <form class="chat-form" id="chatForm">
          <input id="chatInput" type="text" autocomplete="off" placeholder="Hỏi về nội dung bài học..." />
          <button type="submit" class="send-btn" id="sendBtn" title="Gửi">➤</button>
        </form>
        <div class="chat-hint">Trả lời bám đúng đoạn bài · Không tiết lộ đáp án quiz</div>
      </div>
    </aside>
  </main>

  <script>
    let LESSONS = [];
    let activeIdx = 0;
    let isPlaying = false;
    let playTimer = null;
    let currentSec = 135;
    const totalSec = 320;
    let rewindCount = 0;
    let tabHiddenAt = null;
    let busy = false;

    const feed = document.getElementById("feed");
    const calmEmpty = document.getElementById("calmEmpty");
    const playerCard = document.getElementById("playerCard");
    const drawer = document.getElementById("drawer");
    const backdrop = document.getElementById("backdrop");
    const traceModal = document.getElementById("traceModal");

    function fmtTime(sec) {
      const s = Math.max(0, Math.min(totalSec, Math.floor(sec)));
      const m = String(Math.floor(s / 60)).padStart(2, "0");
      const r = String(s % 60).padStart(2, "0");
      return `${m}:${r}`;
    }

    function updatePlayerUI() {
      document.getElementById("progressFill").style.width = `${(currentSec / totalSec) * 100}%`;
      document.getElementById("timeLabel").textContent = `${fmtTime(currentSec)} / ${fmtTime(totalSec)}`;
      document.getElementById("playBtn").textContent = isPlaying ? "⏸ Tạm dừng" : "▶ Tiếp tục học";
    }

    function selectLesson(idx, pulse = false) {
      activeIdx = idx;
      rewindCount = 0;
      const l = LESSONS[activeIdx];
      if (!l) return;

      document.getElementById("bannerTitle").textContent = `${l.day} · ${l.topic}`;
      document.getElementById("topicTitle").textContent = l.topic;
      document.getElementById("slideTag").textContent = `${l.day} · Mã đoạn ${l.code}`;
      document.getElementById("slideTitle").textContent = l.title;
      document.getElementById("slideText").textContent = l.content;

      renderQuiz(l);
      renderDrawer();

      if (pulse) {
        playerCard.classList.remove("highlight");
        void playerCard.offsetWidth;
        playerCard.classList.add("highlight");
        setTimeout(() => playerCard.classList.remove("highlight"), 2000);
      }
    }

    function renderQuiz(lesson) {
      const card = document.getElementById("quizCard");
      const fb = document.getElementById("quizFeedback");
      fb.textContent = "";
      fb.className = "quiz-feedback";
      if (!lesson.quiz) {
        card.classList.add("hidden");
        return;
      }
      card.classList.remove("hidden");
      document.getElementById("quizQuestion").textContent = lesson.quiz.question;
      const optsBox = document.getElementById("quizOpts");
      const letters = ["A", "B", "C", "D"];
      optsBox.innerHTML = lesson.quiz.options.map((opt, i) =>
        `<button type="button" class="quiz-opt" data-idx="${i}"><strong>${letters[i]}.</strong> ${opt}</button>`
      ).join("");

      optsBox.querySelectorAll(".quiz-opt").forEach(btn => {
        btn.addEventListener("click", () => {
          optsBox.querySelectorAll(".quiz-opt").forEach(b => b.classList.remove("correct", "wrong"));
          const picked = Number(btn.dataset.idx);
          if (picked === lesson.quiz.correct) {
            btn.classList.add("correct");
            fb.textContent = "Chính xác! Bạn đã nắm đúng ý cốt lõi của đoạn này.";
            fb.className = "quiz-feedback ok";
          } else {
            btn.classList.add("wrong");
            fb.textContent = "Chưa đúng — xem gợi ý ngắn bên phải để tự suy luận lại nhé.";
            fb.className = "quiz-feedback err";
            const payload = `Bài: ${lesson.day} | Đoạn: ${lesson.code} (${lesson.topic} — ${lesson.title}) | Hành vi: vừa làm sai câu kiểm tra lần 1, dừng 40s | Quiz: sai lần 1 | Tin nhắn HV: Mình vừa chọn sai câu hỏi về ${lesson.title}, gợi mở ngắn giúp mình tự hiểu lại bản chất mà không lộ đáp án`;
            askAgent(payload, `Bạn vừa làm sai câu kiểm tra ở ${lesson.code}`);
          }
        });
      });
    }

    function renderDrawer() {
      const groups = {};
      LESSONS.forEach((l, i) => {
        if (!groups[l.day]) groups[l.day] = { topic: l.topic, items: [] };
        groups[l.day].items.push({ ...l, idx: i });
      });
      const list = document.getElementById("drawerList");
      list.innerHTML = Object.entries(groups).map(([day, g]) => `
        <div class="day-hdr"><span class="d-num">${day.replace("Day ", "D")}</span><span>${g.topic}</span></div>
        ${g.items.map(it => `
          <button type="button" class="seg-btn ${it.idx === activeIdx ? 'active' : ''}" data-idx="${it.idx}">
            <span class="seg-dot"></span>
            <div>
              <div class="seg-t">${it.title}</div>
              <div class="seg-c">${it.code}</div>
            </div>
          </button>
        `).join("")}
      `).join("");
      list.querySelectorAll(".seg-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          selectLesson(Number(btn.dataset.idx));
          drawer.classList.add("hidden");
          backdrop.classList.add("hidden");
        });
      });
    }

    function cleanOutput(raw) {
      const lines = (raw || "").split("\n").map(s => s.trim()).filter(Boolean);
      const kept = lines.filter(l => !l.startsWith("[Thẻ gỡ kẹt") && !l.startsWith("(Gợi ý bên lề"));
      return kept.length ? kept.join("\n") : (raw || "");
    }

    function renderTrace(data) {
      const s = data.summary || {};
      document.getElementById("traceSummary").textContent =
        `Model: ${(s.models && s.models.join(", ")) || "rule-only (0 token)"}\n` +
        `Model calls: ${s.model_calls ?? 0} | Tool calls: ${s.tool_calls ?? 0}\n` +
        `Tokens in/out: ${s.tokens_in ?? 0} / ${s.tokens_out ?? 0} | Latency: ${data.latency_s}s`;
      const box = document.getElementById("traceList");
      box.innerHTML = "";
      (data.events || []).forEach(ev => {
        const div = document.createElement("div");
        div.className = "trace-ev";
        div.textContent = ev.kind === "note"
          ? `[NOTE] ${ev.text}`
          : ev.kind === "model"
            ? `[MODEL ${ev.model}] in=${ev.tokens_in} out=${ev.tokens_out} (${ev.latency_s}s)`
            : `[TOOL ${ev.name}] ${ev.output || ""}`;
        box.appendChild(div);
      });
    }

    async function askAgent(payload, userNote = "") {
      if (busy) return;
      busy = true;
      calmEmpty.classList.add("hidden");

      if (userNote) {
        const u = document.createElement("div");
        u.className = "user-msg";
        u.textContent = userNote;
        feed.appendChild(u);
      }

      const waitEl = document.createElement("div");
      waitEl.className = "quiet-note";
      waitEl.textContent = "Đang đọc đoạn bài...";
      feed.appendChild(waitEl);
      feed.scrollTop = feed.scrollHeight;
      document.getElementById("sendBtn").disabled = true;

      try {
        const res = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: payload })
        });
        const data = await res.json();
        waitEl.remove();
        renderTrace(data);

        if (data.error) {
          const e = document.createElement("div");
          e.className = "ai-card kind-refuse";
          e.textContent = "Không gọi được trợ lý: " + data.error;
          feed.appendChild(e);
        } else if (data.meta.kind === "silent") {
          const q = document.createElement("div");
          q.className = "quiet-note";
          q.textContent = "Trợ lý giữ im lặng để không làm đứt mạch học của bạn.";
          feed.appendChild(q);
        } else {
          const card = document.createElement("div");
          card.className = `ai-card kind-${data.meta.kind}`;

          const top = document.createElement("div");
          top.className = "ai-card-top";
          const lbl = document.createElement("span");
          lbl.className = "ai-label";
          lbl.textContent = data.meta.label;
          const x = document.createElement("button");
          x.type = "button"; x.className = "dismiss-btn"; x.textContent = "Đã hiểu ✕";
          x.onclick = () => card.remove();
          top.append(lbl, x);

          const txt = document.createElement("div");
          txt.className = "ai-text";
          txt.textContent = data.meta.kind === "card" ? cleanOutput(data.output) : data.output;
          card.append(top, txt);

          if (data.meta.kind !== "abstain" && (data.meta.codes || []).length > 0) {
            const acts = document.createElement("div");
            acts.className = "ai-actions";
            data.meta.codes.forEach(c => {
              const btn = document.createElement("button");
              btn.type = "button"; btn.className = "cite-chip";
              btn.textContent = `Xem lại đoạn ${c}`;
              btn.onclick = () => {
                const idx = LESSONS.findIndex(item => item.code === c);
                if (idx >= 0) selectLesson(idx, true);
              };
              acts.appendChild(btn);
            });
            card.appendChild(acts);
          }

          feed.appendChild(card);
          if (data.meta.kind === "card" && (data.meta.codes || []).length > 0) {
            const idx = LESSONS.findIndex(item => item.code === data.meta.codes[0]);
            if (idx >= 0) selectLesson(idx, true);
          }
        }
        feed.scrollTop = feed.scrollHeight;
      } catch (err) {
        waitEl.remove();
        const e = document.createElement("div");
        e.className = "ai-card kind-refuse";
        e.textContent = "Lỗi kết nối: " + err;
        feed.appendChild(e);
      } finally {
        busy = false;
        document.getElementById("sendBtn").disabled = false;
      }
    }

    // PHÁT / DỪNG THANH TIẾN ĐỘ ĐƠN GIẢN
    document.getElementById("playBtn").addEventListener("click", () => {
      isPlaying = !isPlaying;
      if (isPlaying) {
        playTimer = setInterval(() => {
          currentSec = currentSec >= totalSec ? 0 : currentSec + 1;
          updatePlayerUI();
        }, 1000);
      } else if (playTimer) {
        clearInterval(playTimer);
      }
      updatePlayerUI();
    });

    // BẤM TUA LẠI THẬT: bấm lần 2 -> tự động kích hoạt gỡ kẹt!
    document.getElementById("rewindBtn").addEventListener("click", () => {
      currentSec = Math.max(0, currentSec - 15);
      updatePlayerUI();
      rewindCount += 1;
      const l = LESSONS[activeIdx];
      if (!l) return;
      if (rewindCount >= 2) {
        rewindCount = 0;
        const payload = `Bài: ${l.day} | Đoạn: ${l.code} (${l.topic} — ${l.title}) | Hành vi: nghe video và đọc slide 2 lần, tua lại 2 lần, dừng 45s | Quiz: chưa làm | Tin nhắn HV: Mình vừa tua lại 2 lần đoạn ${l.title} vẫn chưa hình dung rõ, giải thích cực ngắn giúp mình`;
        askAgent(payload, `Bạn vừa tua lại đoạn ${l.code} 2 lần`);
      } else {
        calmEmpty.classList.add("hidden");
        const q = document.createElement("div");
        q.className = "quiet-note";
        q.textContent = "Bạn vừa tua lại 1 lần — trợ lý chưa xen vào để giữ mạch học.";
        feed.appendChild(q);
        feed.scrollTop = feed.scrollHeight;
      }
    });

    // PHÁT HIỆN CHUYỂN TAB THẬT TRÊN TRÌNH DUYỆT -> KHÔNG XEN VÀO!
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        tabHiddenAt = Date.now();
      } else if (tabHiddenAt) {
        const awaySec = Math.max(5, Math.round((Date.now() - tabHiddenAt) / 1000));
        tabHiddenAt = null;
        const l = LESSONS[activeIdx];
        if (!l) return;
        const payload = `Bài: ${l.day} | Đoạn: ${l.code} | Hành vi: dừng ${awaySec}s, chuyển sang tab khác đi việc riêng (blur window) | Quiz: chưa làm | Tin nhắn HV: (không có)`;
        askAgent(payload, "");
      }
    });

    // GÕ CÂU HỎI TỰ NHIÊN Ở Ô CHAT
    document.getElementById("chatForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const input = document.getElementById("chatInput");
      const msg = input.value.trim();
      if (!msg) return;
      input.value = "";
      const l = LESSONS[activeIdx];
      // Chỉ gắn mã đoạn hiện tại nếu câu quá ngắn/mơ hồ hoặc hỏi trực tiếp quiz/đáp án;
      // các câu hỏi khái niệm tự do để search_lesson tự tra toàn kho 12 đoạn (hoặc báo G10 nếu ngoài bài).
      const refersCurrent = msg.length <= 20 || /(quiz|đáp án|đoạn này|câu này)/i.test(msg);
      const segPart = (l && refersCurrent)
        ? `${l.code} (${l.topic} — ${l.title})`
        : "(không có đoạn bài tương ứng trong dữ liệu)";
      const payload = `Bài: ${l ? l.day : "Day 08"} | Đoạn: ${segPart} | Hành vi: dừng 45s | Quiz: chưa làm | Tin nhắn HV: ${msg}`;
      askAgent(payload, msg);
    });

    // CHẠY CÂU THỬ TỰ DO TRONG MODAL TRACE (dành cho giám khảo)
    document.getElementById("judgeRunBtn").addEventListener("click", () => {
      const txt = document.getElementById("judgeInput").value.trim();
      if (!txt) return;
      traceModal.classList.add("hidden");
      askAgent(txt, txt);
    });

    // ĐIỀU HƯỚNG & MODAL
    document.getElementById("openDrawerBtn").addEventListener("click", () => {
      drawer.classList.remove("hidden");
      backdrop.classList.remove("hidden");
    });
    document.getElementById("closeDrawerBtn").addEventListener("click", () => {
      drawer.classList.add("hidden");
      backdrop.classList.add("hidden");
    });
    backdrop.addEventListener("click", () => {
      drawer.classList.add("hidden");
      backdrop.classList.add("hidden");
    });
    document.getElementById("openTraceBtn").addEventListener("click", () => {
      traceModal.classList.toggle("hidden");
    });
    document.getElementById("closeTraceBtn").addEventListener("click", () => {
      traceModal.classList.add("hidden");
    });
    document.getElementById("nextBtn").addEventListener("click", () => {
      if (!LESSONS.length) return;
      selectLesson((activeIdx + 1) % LESSONS.length);
    });

    async function init() {
      const res = await fetch("/api/lessons");
      LESSONS = await res.json();
      const d08 = LESSONS.findIndex(l => l.code === "D08-S01");
      selectLesson(d08 >= 0 ? d08 : 0);
      updatePlayerUI();
    }
    init();
  </script>
</body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def log_message(self, format_str, *args):
        pass

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_text, status=200):
        body = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_html(HTML_PAGE)
            return
        if self.path == "/api/lessons":
            self._send_json(load_lessons())
            return
        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        if self.path != "/api/ask":
            self._send_json({"error": "Not found"}, status=404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace")
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self._send_json({"error": "JSON đầu vào không hợp lệ"}, status=400)
            return
        text = str(body.get("text") or "").strip()
        if not text:
            self._send_json({"error": "Thiếu nội dung đầu vào"}, status=400)
            return
        self._send_json(run_agent_traced(text))


def main():
    parser = argparse.ArgumentParser(description="Preclass Online — Adaptive Scaffolding Web Demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"
    server = ThreadingHTTPServer((args.host, args.port), DemoHandler)
    print(f"Preclass Online Web Demo: {url}")
    print("Nhấn Ctrl+C để dừng.")
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
