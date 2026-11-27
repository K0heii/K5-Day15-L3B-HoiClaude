# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ Đã đạt ngưỡng | [`evidence/data-mining.md`](data-mining.md) · [`evidence/count.py`](count.py) |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ Đang làm (1/4 xong: `P1`) | [`evidence/interviews/P1.md`](interviews/P1.md) *(đang chờ `P2`–`P4`)* |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Không dùng làm nguồn chính | — |

## 2. Số chính

- **Đào data (`data/preclass/`, 05/11–25/11/2026, `N = 436` HV hoạt động):**
  - **174 / 436 HV (39,9%)** có ≥1 dấu hiệu kẹt rõ *(tua ngược ≥2 lần, dừng ≥3 lần/quãng, hoặc làm sai lần đầu)* — trung vị **8 lần/21 ngày (~11,4 lần/tháng)**.
  - **2.224 / 3.900 cặp `(hv, video)` (57,0%)** mở ra nhưng không xem hết; **2.602 / 4.322 lượt tua (60,2%)** là tua ngược.
  - **424 / 2.478 câu lần đầu làm sai (17,1%)**, vọt lên **36,0% ở Day 06** (41/114) và **41,4% ở Day 13** (12/29); chỉ **9/424 (2,1%)** được thưởng `sua_sai`.
  - **887 / 1.260 phản hồi AI (70,4%)** không có mốc trích dẫn; **909 / 1.223 lượt hỏi (74,3%)** thụ động (`rubric_y_moi=0`); **435 / 436 HV (99,8%)** có rời tab; lời AI bạn học tự xen vào **13.975 lần** chỉ được phản hồi **91 lần (0,65%)**.
- **Phỏng vấn *(đang cập nhật, n nhỏ không ghi %)*:** 1/1 người đã hỏi (`P1`) gặp rõ pain ở bài Day 06 · số lần kẹt nặng/tháng: `P1` 1–2 lần · mỗi lần mất `15–30 phút` *(đang tiếp tục bổ sung `P2`–`P4`)*.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên L3 (học tối 20h–24h đều đặn) | Có (bài Day 06) | 1–2 lần (kẹt nặng) | 15–30 phút (cuốn đi >30 phút) | Chatbot dưới bài + mở tab ChatGPT |
| P2 | *(đang hỏi — Minh)* | | | | |
| P3 | *(đang hỏi — Hiệp)* | | | | |
| P4 | *(đang hỏi — Quang)* | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. *"Lần ở bài Day 06 đó mình mở tab ngoài hỏi ChatGPT, xong đọc tài liệu liên quan bị cuốn đi mất hơn 30 phút. Đến lúc quay lại trang pre-class thì quên mất mạch bài giảng phía trước, xem tiếp video bị trôi tuột, cuối cùng làm câu quiz kiểm tra bị sai mất 1 câu."* — **P1** (`evidence/interviews/P1.md`)
2. *"Gây phiền nhất là tự nhiên nhảy pop-up che màn hình lúc mình đang tập trung đọc code. Lúc kẹt thật, mình chỉ cần 1 ví dụ đời thường ngắn gọn hoặc 1 sơ đồ so sánh 2 cột để thấy ngay sự khác biệt là hiểu liền."* — **P1** (`evidence/interviews/P1.md`)
3. **Bỏ qua quiz rồi tua ngược ngay 3 giây sau:** `L0503` bỏ qua câu hỏi giữa video lúc `20:32` VN (`skipped_stop=True`) và lập tức tua ngược 23,8 giây (`241.3s → 217.5s`) — **dòng 195–196 `events.csv`** (`evidence/data-mining.md`)
4. **Làm sai liên tiếp 3 câu trong 3 phút ở bài Day 06:** `L0597` sai liền 3 câu lần đầu (`A00161`, `A00883`, `A01376`) lúc `18:44–18:47` VN trên `program-day06:data-engineering-for-agents` — **`answers.csv`** (`evidence/data-mining.md`)
5. **Dừng liên tục 3 lần + rời tab trong 1 quãng xem tối:** `L0010` có `pauses=3, hidden_count=1` trên `d01-r1-v01` lúc `21:10` VN — **dòng 1979 `events.csv`** (`evidence/data-mining.md`)
6. **AI trả lời dài cho câu hỏi 2 ký tự lạc đề & thiếu mốc trích dẫn:** `C01056` (`L0057`, hỏi 2 ký tự, `bam_bai=0`, AI đáp 171 ký tự) và `C00983` (`L0213`, `missing_context=True`, `moc_trich_dan` rỗng) — **`chat.csv` & dòng 112 `events.csv`** (`evidence/data-mining.md`)

*(Sẽ bổ sung thêm trích dẫn nguyên văn từ `P2`, `P3`, `P4` trước CP3.)*

## 4. Các nguồn có khớp nhau không

- **Khớp rất chặt:**
  - Data chỉ ra **Day 06** là một trong 2 bài có tỉ lệ sai lần đầu cao nhất (**36,0%**) → `P1` kể tự nhiên đúng lần kẹt nặng nhất ở bài **Day 06**, mở tab ChatGPT bị cuốn mất >30 phút rồi làm sai câu quiz.
  - Data chỉ ra **70,4% phản hồi AI thiếu mốc trích dẫn** → `P1` giải thích vì sao: *"chatbot dưới chân trang pre-class trả lời hơi chung chung kiểu lý thuyết sách giáo khoa, không giải thích trúng ví dụ trong slide"*.
  - Data chỉ ra **99,8% HV rời tab** và **99,35% lời AI tự xen vào bị phớt lờ** (`91/13.975`) → `P1` xác nhận trực tiếp: *"Gây phiền nhất là tự nhiên nhảy pop-up che màn hình lúc mình đang tập trung đọc code"*.
- **Điểm tinh chỉnh:** Data ghi nhận trung vị 8 lần tín hiệu vi mô/21 ngày, còn `P1` nhớ 1–2 lần *kẹt nặng* tốn 15–30 phút/tháng → nhóm tách rõ *tín hiệu vi mô (tua/dừng)* để kích hoạt bộ lọc vs *ca kẹt nặng thực sự* khi ước lượng Impact.

## 5. Kết luận

Giả thuyết ở [`evidence/hypothesis.md`](hypothesis.md): **đúng phần cốt lõi, cần tinh chỉnh điều kiện kích hoạt** — pain kẹt kiến thức kỹ thuật, mất mạch khi chuyển tab ngoài và câu trả lời AI thiếu gắn bài đều đã có bằng chứng khớp giữa data thật (`data/preclass/`) và phỏng vấn `P1`; tuy nhiên cần lọc chặt nhiễu rời tab và không bật pop-up che màn hình. **Điều vẫn chưa biết (cần kiểm qua `P2`–`P4`):** mức phổ biến của nhóm học viên ít kẹt / học lướt và thời gian mất trung vị trên ≥3 người dùng ngoài nhóm.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3 (`P1`, học tối đều đặn) | 27/11/2026 17:45 | ☑ Đã xong (`P1.md`) |
| Học viên L3 (`P2` — Minh hỏi) | 27/11/2026 18:00–18:30 | ☐ Đang hỏi |
| Học viên L3 (`P3` — Hiệp hỏi) | 27/11/2026 18:00–18:30 | ☐ Đang hỏi |
| Học viên L3 (`P4` — Quang hỏi) | 27/11/2026 18:00–18:30 | ☐ Đang hỏi |
