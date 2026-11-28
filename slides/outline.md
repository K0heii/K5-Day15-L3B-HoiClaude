# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số (`174/436` có dấu hiệu kẹt rõ, `70,4%` phản hồi AI thiếu mốc trích dẫn) và trích dẫn `P1` | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn (`~140 giờ/tháng` trên khối L3) + hướng bị loại (Webcam/Extension) | `spec.md` §2 | ☑ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ 4 bước · AI gợi ý bên lề, học viên tự quyết | `spec.md` §4 | ☑ |
| 4 | Demo live | 1 ca thường (`B01` đang kẹt → ẩn dụ kèm `[D08-S01]`) + 1 ca khó (`B07` rời tab → `[Không xen vào]`); mạng hỏng → video dự phòng | `eval/benchmark.csv`, `eval/run-3.csv` | ☑ |
| 5 | **Đánh giá thế nào** | Dataset · 24 câu thử · 4 metric · lượt 1 (`18/24 = 75%`) → lượt 3 sau cải tiến (`24/24 = 100%`) so với chuẩn "đạt" ≥80% · lỗi chính | `eval/README.md`, `eval/report.md`, `spec.md` §7 | ☑ |
| 6 | **Chi phí khi dùng thật** | 50/50 phiên không lỗi · chi phí / task đạt (`$0.00037` Flash-Lite / `$0.0014` Hydrogen) · 3 kịch bản (300/700/1.000 HV) · so với impact | `cost/cost-estimate.md`, `cost/simulate-2-summary.md` | ☑ |
| 7 | Kết luận | Tiếp tục thí điểm có đo lường với học viên thật, chưa triển khai rộng — dẫn số `39,9%`, `24/24`, `$1.70/tháng` | `evidence/summary.md`, `eval/report.md`, `cost/cost-estimate.md` | ☑ |
| 8 | Nếu có thêm 1 tuần | 3 việc: thử câu hỏi diễn đạt vòng vo/không dấu · mở rộng kho bài vượt 12 đoạn · đo tín hiệu mở/gạt thẻ trên học viên thật | `eval/report.md` mục 4 · `data/DATA_CARD.md` | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| Trang 1–2 (Người dùng, Pain & Impact) | Nguyễn Như Duy An (`2A202603783`) |
| Trang 3–4 (Giải pháp & Demo live `B01`, `B07`) | Nguyễn Minh Quang (`2A202603791`) |
| Trang 5 (Đánh giá `75% → 100%` & Lỗi chính) | Đào Văn Hiệp (`2A202603813`) |
| Trang 6 & Trang 8 (Chi phí 50 phiên & Hướng 1 tuần) | Lã Thái Minh (`2A202603756`) |
| Trang 7 (Kết luận & Điều phối Q&A) | Nguyễn Như Duy An (`2A202603783`) |
