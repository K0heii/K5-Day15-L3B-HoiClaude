# Reflection — Nguyễn Như Duy An

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Vai trò: **Đội trưởng (`2A202603783`)** — chịu trách nhiệm khởi tạo khung repo, lập kế hoạch chia việc cho 4 thành viên (`docs/team-plan.md`, commit `2c48047`), nộp các mốc checkpoint CP1–CP4, trực tiếp thực hiện phần bằng chứng pain, bảng Impact và đồng bộ repo.
   - Các đầu việc trực tiếp thực hiện: điền chuẩn `TEAMS.md`, `canvas.md`, `evidence/hypothesis.md`, `docs/interview-form.md` (`dbaa8e2`, `0a6e8a7`); viết script đào bộ dữ liệu hành vi thật `data/preclass/` (`evidence/count.py`, `evidence/data-mining.md`), phỏng vấn `evidence/interviews/P1.md`, tổng hợp đủ 4 người phỏng vấn `P1–P4` vào `evidence/summary.md` và tính bảng Impact ở `spec.md §1–§2` (`5b8921a`, `d882c1d`); cấu hình `.env` nối model thật `gemini-3.5-flash-lite` để chạy Lượt 1 `eval/run-1.csv` (`0c5c0f6`) và cập nhật `README.md`, `docs/ai-usage.md` (`9fa5e94`).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Công cụ sử dụng: **Antigravity (Gemini)** để rà soát yêu cầu từng checkpoint, sinh khung script `evidence/count.py` đọc `events.csv` (107.709 dòng) bằng thư viện chuẩn Python, kiểm tra lỗi định dạng và đối chiếu chéo file giữa 4 thành viên.
   - Các chỗ mình phải trực tiếp kiểm tra và chỉnh lại: (1) tự kiểm mẫu số trong `evidence/count.py` để dùng đúng **436 học viên hoạt động** thay vì 721 tài khoản tạo sẵn; (2) phát hiện và yêu cầu nhóm xử lý lỗi lệch mã đoạn giữa `data/lessons.json` với `eval/benchmark.csv` cũng như loại bỏ phiếu `P4` bị trùng với `P3` trước khi chốt CP2; (3) tự điều chỉnh công thức Impact ở `spec.md §2` theo số phút thật từ phỏng vấn (`15 phút/lần`, ~140 giờ/tháng) và rà soát không để lọt `.env` hay file CSV gốc của BTC lên GitHub.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Ở Lượt 1 (`eval/run-1.csv`, đạt 18/24 = 75%), nhóm lỗi khiến mình chú ý nhất là **Nhóm 1 (`B03`, `B08`, `B19`)**: học viên chỉ đang đọc bình thường hoặc ghi chép (`"chưa tua lại"`, `"không tua lại"`, `"không làm sai quiz"`), nhưng hệ thống vẫn bật thẻ gỡ kẹt vì hàm `parse_learner_signal()` trong `codebase/tools.py` chỉ tìm chuỗi con `"tua lại"` / `"làm sai"` mà bỏ qua từ phủ định đứng trước.
   - Bài học rút ra: với sản phẩm AI chủ động hỗ trợ học tập, lỗi **báo nhầm (False Positive)** đau hơn lỗi bỏ sót vì làm đứt mạch tập trung đúng như `P1` và `P3` phản ánh (*"hiện pop-up bất ngờ gây bực"*). Khi sửa tổng quát phần xử lý cụm phủ định (cùng 2 lỗi G10 ngoài bài `B06/B22` và chặn nhầm khái niệm `B18`) thay vì vá cứng theo câu thử, Lượt 3 (`eval/run-3.csv`) mới đạt 24/24 (100%) và giữ được nguyên tắc thiết kế G10.
