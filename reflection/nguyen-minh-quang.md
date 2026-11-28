# Reflection — Nguyễn Minh Quang

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách Kiến trúc AI, Dữ liệu bài học và Lõi `codebase/` trong nhóm HoiClaude (`L3B · Track A`). Cụ thể mình đã hoàn thiện `spec.md` (§3–§4 và cập nhật §10 changelog), biên soạn 12 đoạn bài học gắn mã `D06-S01`–`D13-S03` kèm `start_s`/`end_s` trong `data/lessons.json` và `data/DATA_CARD.md`, thực hiện khảo sát `evidence/interviews/P4.md`, và xây dựng luồng workflow cố định 4 bước với 5 chốt chặn an toàn trong `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py` (nối model thật `gemini-3.5-flash-lite` chạy `eval/run-3.csv` đạt `24/24`).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Mình dùng trợ lý coding AI (Antigravity / Gemini) để rà soát cấu trúc repo, lên khung mã nguồn Python chuẩn PEP 8, viết script kiểm thử 24 câu và giải mã dữ liệu khảo sát. Tuy nhiên mình phải trực tiếp kiểm tra và sửa lại nhiều chỗ: sửa lỗi AI sinh bộ lọc từ khoá ban đầu ở `search_lesson()` làm khớp nhầm từ phổ thông tiếng Việt, sửa lỗi sót biến sau khi gộp code ở `tools.py`, chỉnh lại thứ tự kiến trúc thực tế từ *DB → Cache* thành *Rule → Cache → DB → LLM*, và chủ động bác bỏ hướng làm Webcam MediaPipe để giữ đúng ranh giới thiết kế không xâm phạm riêng tư ở `spec.md §4`.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   Ở Lượt 1 (`eval/run-1.csv`, đạt `18/24 = 75%`), câu `B03` và `B08` bị trượt vì học viên đang đọc bình thường / ghi chép (`"chưa tua lại"`, `"không tua lại"`) nhưng `parse_learner_signal()` lại khớp chuỗi con `"tua lại"` và bật thẻ gỡ kẹt gây phiền. Từ lỗi này (cùng với `B06` không kích hoạt G10 và `B18` bị chặn nhầm câu hỏi *"Tại sao..."*), mình học được rằng không thể phó mặc cho prompt hay khớp từ khoá đơn giản — phải tách riêng vùng quét hành vi khỏi tiêu đề bài, tính trọng số IDF cho tìm kiếm và bọc thêm lớp hậu kiểm đầu ra bằng code.
