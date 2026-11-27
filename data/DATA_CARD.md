# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.

## Dataset 1 · `data/lessons.json` (Kho đoạn bài học pre-class AI20K rút gọn)

| | |
|---|---|
| Dùng để làm gì | Nguồn căn cứ cho công cụ `search_lesson` trong `codebase/tools.py` và đối chiếu trích mã đoạn `[DXX-SYY]` trong bộ câu thử |
| Từ đâu | Nhóm tự viết lại / tóm tắt khái niệm cốt lõi dựa trên khung chủ đề bài học AI20K K5 (Day 06, Day 08, Day 10, Day 12, Day 13) — **không** commit nguyên tài liệu khoá |
| Xử lý những bước gì | Chia theo đơn vị ý cốt lõi (chunk) · gắn mã đoạn duy nhất (`D06-S01`…`D13-S03`) · thêm từ khoá tìm kiếm và bẫy hiểu nhầm thường gặp |
| Số dòng / số đoạn | 12 đoạn (`D06-S01`–`D06-S03`, `D08-S01`–`D08-S02`, `D10-S01`–`D10-S02`, `D12-S01`–`D12-S02`, `D13-S01`–`D13-S03`) |
| Phiên bản / ngày lấy | v1.0 · 27/11/2026 |
| Nhãn | `synthetic` (nội dung diễn giải/viết lại ngắn gọn phục vụ bản chạy thử) |
| Giới hạn | Chưa phủ toàn bộ các ngày học của khoá AI20K; mới tập trung vào 5 chủ điểm kỹ thuật nặng hay gặp ở L3. Không dùng để làm bằng chứng pain. |

**Ghi chú kiểm duyệt dữ liệu tự viết (`synthetic`):** Do Nguyễn Minh Quang biên soạn và rà soát toàn bộ 12/12 đoạn để đảm bảo khớp thuật ngữ khoá học, không chứa đáp án quiz thật và không sao chép nguyên văn tài liệu BTC.

---

## Dataset 2 · `data/preclass/` (Dữ liệu hành vi học viên thật BTC cấp — chỉ lưu cục bộ)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain thực tế (`evidence/data-mining.md`, `evidence/summary.md`) và lấy mẫu ngữ cảnh cho bộ câu thử (`source: data_that`) |
| Từ đâu | Bộ dữ liệu BTC cấp (`answers.csv`, `chat.csv`, `events.csv`, `learners.csv`, `completed_items.csv`) |
| Xử lý những bước gì | Tổng hợp thống kê ở máy cá nhân · ẩn danh hoàn toàn mã học viên trước khi trích ví dụ · **không** commit file gốc lên Git |
| Số dòng / số đoạn | 2.478 lượt trả lời (`answers.csv`), 1.223 lượt chat đã chấm (`chat.csv`), nhật ký sự kiện (`events.csv`) |
| Phiên bản / ngày lấy | Bản BTC cấp · 27/11/2026 |
| Nhãn | thật |
| Giới hạn | Log hành vi cho biết người học làm gì (làm sai, hỏi ngắn, dừng/chuyển trang) nhưng không giải thích trực tiếp nguyên nhân chủ quan; cần đối chiếu chéo qua phỏng vấn (`evidence/interviews/P1–P4.md`). |
