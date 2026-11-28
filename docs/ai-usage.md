# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude / Gemini (Antigravity) | Gợi ý cấu trúc workflow 4 bước (`agent.py`, `tools.py`, `ai.py`), giao diện Web Demo cục bộ (`web_demo.py`) và kết nối REST API các hãng | Đọc hiểu toàn bộ code, chạy kiểm thử 12→24 câu benchmark, chỉnh sửa logic guardrail (`a9ed75d`), kiểm tra trực quan Web Demo và nối `.env` thật | Nguyễn Minh Quang · Nguyễn Như Duy An |
| Prompt / thiết kế lời gọi mô hình | Claude / Gemini | Gợi ý nháp `SYSTEM` prompt giới hạn 3 kiểu gỡ kẹt và ép trích mã đoạn `[DXX-SYY]` | Rà soát điều kiện cấm lộ đáp án, chạy thực tế trên `gemini-3.5-flash-lite` và đối chiếu trace (`run-1`–`run-3`) | Nguyễn Minh Quang |
| Đào data (viết script đếm, gợi ý nhãn) | Gemini (Antigravity) | Viết script thư viện chuẩn `evidence/count.py` đọc `events.csv`, `answers.csv`, `chat.csv` | Kiểm tay cách đặt mẫu số (436 HV hoạt động, 2.478 câu `lan_thu=1`), chạy lại đối chiếu 6/6 ví dụ dòng ẩn danh thật | Nguyễn Như Duy An |
| Rà câu hỏi phỏng vấn / khảo sát | Gemini (Antigravity) | Chỉ rà câu dẫn dắt theo quy tắc Mom Test (`docs/interview-form.md`) | Tự đi hỏi và thu thập phản hồi từ 4 học viên L3 thật ngoài nhóm (`P1`–`P4`), tự kiểm ẩn danh và giữ nguyên trích dẫn | Cả 4 thành viên (`P1` An · `P2` Minh · `P3` Hiệp · `P4` Quang) |
| Viết câu thử (benchmark) | Claude / Gemini | Hỗ trợ rà độ phủ lưới input 4 chiều và format CSV | Mỗi câu thử có `source` rõ ràng (11/24 từ người dùng/data thật); tự duyệt từng `expected` và `pass_criterion`, chốt cứng chuẩn đạt trước CP2 | Đào Văn Hiệp |
| Sinh data `synthetic` (nếu có) | Claude / Gemini | Hỗ trợ tóm tắt khung 12 đoạn bài học đánh mã đoạn (`data/lessons.json`) | Không dùng làm bằng chứng pain; kiểm tay 12/12 đoạn khớp thuật ngữ khoá học và không chứa đáp án quiz thật (`data/DATA_CARD.md`) | Nguyễn Minh Quang |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng LLM chấm tự động | Không dùng | Chấm thủ công 100% cả 3 lượt (`run-1.csv`, `run-2.csv`, `run-3.csv`) theo `eval/metric_spec.yaml` và chạy `python run.py score` | Đào Văn Hiệp · Lã Thái Minh |
| Slide, văn bản | Claude / Gemini | Hỗ trợ dàn HTML/CSS cho `slides/demo.html` → `demo-slides.pdf` và rà nhất quán số liệu giữa `spec.md`, `canvas.md`, `eval/`, `cost/` | Tự duyệt toàn bộ con số, nguồn trích dẫn, bố cục 8/8 trang PDF và chịu trách nhiệm trình bày khi demo | Nguyễn Như Duy An · Lã Thái Minh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
