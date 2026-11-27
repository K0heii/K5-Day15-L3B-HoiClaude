# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ Đã đạt ngưỡng | [`evidence/data-mining.md`](data-mining.md) · [`evidence/count.py`](count.py) |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ Đã đạt ngưỡng (4/4 người: `P1`–`P4`) | [`P1.md`](interviews/P1.md) · [`P2.md`](interviews/P2.md) · [`P3.md`](interviews/P3.md) · [`P4.md`](interviews/P4.md) |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Không dùng làm nguồn chính | — |

## 2. Số chính

- **Đào data (`data/preclass/`, 05/11–25/11/2026, `N = 436` HV hoạt động):**
  - **174 / 436 HV (39,9%)** có ≥1 dấu hiệu kẹt rõ *(tua ngược ≥2 lần, dừng ≥3 lần/quãng, hoặc làm sai lần đầu)* — trung vị **8 lần/21 ngày (~11,4 lần/tháng)**.
  - **2.224 / 3.900 cặp `(hv, video)` (57,0%)** mở ra nhưng không xem hết; **2.602 / 4.322 lượt tua (60,2%)** là tua ngược.
  - **424 / 2.478 câu lần đầu làm sai (17,1%)**, vọt lên **36,0% ở Day 06** (41/114) và **41,4% ở Day 13** (12/29); chỉ **9/424 (2,1%)** được thưởng `sua_sai`.
  - **887 / 1.260 phản hồi AI (70,4%)** không có mốc trích dẫn; **909 / 1.223 lượt hỏi (74,3%)** thụ động (`rubric_y_moi=0`); **435 / 436 HV (99,8%)** có rời tab; lời AI bạn học tự xen vào **13.975 lần** chỉ được phản hồi **91 lần (0,65%)**.
- **Phỏng vấn *(n = 4, không ghi % theo guide 1.2)*:** **4/4 người ngoài nhóm** gặp rõ pain khi học pre-class · số lần kẹt nặng / tháng: `P1` 1–2 lần, `P2` 1–2 lần, `P3` 1–2 lần, `P4` >5 lần · mỗi lần tự xoay xở tốn `5–30 phút` (trung vị **~10–15 phút** trên `P1–P3`; riêng `P4` bỏ dở luôn không xem tiếp).

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên L3 (học tối 20h–24h đều đặn) | Có (bài Day 06 Chunking) | 1–2 lần | 15–30 phút (cuốn đi >30 phút) | Chatbot dưới bài + mở tab ChatGPT |
| P2 | Học viên L3 đi làm (học tối 20h–24h đều đặn) | Có (bài Day 13 Unit Economics) | 1–2 lần | 5–15 phút (~10 phút) | Tua video + chatbot dưới bài + ChatGPT/Claude |
| P3 | Học viên L3 (học tối 20h–24h đều đặn) | Có (bài Day 06 RAG) | 1–2 lần | 5–15 phút | Tua video + chatbot + ChatGPT/Claude/Gemini + Google + hỏi bạn/Discord |
| P4 | Học viên L3 (học pre-class hiếm khi) | Có (thường xuyên) | >5 lần | Bỏ dở không xem tiếp | Bỏ qua luôn đoạn khó |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. *"Lần ở bài Day 06 đó mình mở tab ngoài hỏi ChatGPT, xong đọc tài liệu liên quan bị cuốn đi mất hơn 30 phút. Đến lúc quay lại trang pre-class thì quên mất mạch bài giảng phía trước, xem tiếp video bị trôi tuột, cuối cùng làm câu quiz kiểm tra bị sai mất 1 câu."* — **P1** (`evidence/interviews/P1.md`)
2. *"Gây phiền nhất là tự nhiên nhảy pop-up che màn hình lúc mình đang tập trung đọc code. Lúc kẹt thật, mình chỉ cần 1 ví dụ đời thường ngắn gọn hoặc 1 sơ đồ so sánh 2 cột để thấy ngay sự khác biệt là hiểu liền."* — **P1** (`evidence/interviews/P1.md`)
3. *"Tôi hỏi nhưng vẫn trả lời chung chung, không đáp ứng được nhu cầu của tôi, vì vậy vẫn phải tab ra ngoài dùng AI chuyên dụng."* — **P2** (`evidence/interviews/P2.md`)
4. *"hiện pop-up bất ngờ gây bực"* / *"mất thời gian, đứt mạch tập trung"* — **P3** (`evidence/interviews/P3.md`)
5. *"mất thời gian"* *(lặp lại ở cả 3 câu hỏi về chỗ bất tiện, trợ giúp hiện tại và điều gây phiền → bỏ qua đoạn khó, bỏ dở không xem tiếp)* — **P4** (`evidence/interviews/P4.md`)
6. **Ví dụ hành vi thật từ log (`events.csv`, `answers.csv`, `chat.csv`):**
   - `L0503` đóng bỏ qua quiz giữa video lúc `20:32` VN rồi lập tức tua ngược 23,8s (`241.3s → 217.5s`) — **dòng 195–196 `events.csv`**.
   - `L0597` làm sai liên tiếp 3 câu lần đầu trong 3 phút ở Day 06 (`A00161`, `A00883`, `A01376`) — **`answers.csv`**.
   - `L0213` nhận phản hồi AI `C00983` có `missing_context=True` và không có mốc trích dẫn — **dòng 112 `events.csv`**.

## 4. Các nguồn có khớp nhau không

- **Khớp rất chặt trên cả 4 chiều:**
  1. **Đúng bài học kẹt nhất:** Data chỉ ra 2 bài có tỉ lệ sai lần đầu cao nhất là **Day 13 (41,4%)** và **Day 06 (36,0%)** → `P1` và `P3` kể kẹt nặng ở **Day 06** (*Chunking*, *RAG*), còn `P2` kể kẹt nặng ở **Day 13** (*Unit Economics*).
  2. **Hậu quả bỏ dở bài:** Data cho thấy **57,0% cặp `(hv, video)` không xem tới cuối** → `P4` xác nhận gặp đoạn khó >5 lần/tháng và chọn **bỏ qua / bỏ dở không xem tiếp** vì thấy mất thời gian.
  3. **Chatbot dưới bài thiếu bám bài:** Data cho thấy **70,4% phản hồi AI thiếu mốc trích dẫn** → cả `P1` và `P2` đều giải thích chatbot dưới bài *"trả lời chung chung, không đúng trọng tâm"* nên buộc phải mở tab ngoài tra ChatGPT/Claude.
  4. **Pop-up đại trà gây phiền:** Data cho thấy **99,8% HV rời tab** và **99,35% lời AI tự xen vào bị phớt lờ** (`91/13.975`) → cả `P1` và `P3` đều phản đối thẳng việc tự nhảy pop-up che màn hình / bật bất ngờ khi đang tập trung đọc bài.
- **Điểm tinh chỉnh từ đối chiếu:** Data đo được trung vị 8 lần tín hiệu vi mô/21 ngày, còn nhóm học đều (`P1–P3`) tự nhớ 1–2 lần *kẹt nặng* tốn 5–30 phút/tháng (riêng `P4` >5 lần/tháng và bỏ dở) → hệ thống phải lọc kỹ tín hiệu vi mô để chỉ can thiệp khi thật sự kẹt, giữ thẻ cực ngắn bên lề để không gây *"mất thời gian"*.

## 5. Kết luận

Giả thuyết ở [`evidence/hypothesis.md`](hypothesis.md): **đúng và đã kiểm chứng chéo qua cả 2 nguồn đạt ngưỡng** (đào data thật `data/preclass/` + 4/4 người phỏng vấn ngoài nhóm `P1–P4`). Cả hai nguồn hội tụ vào cùng 3 yêu cầu cốt lõi cho giải pháp: (1) lọc nhiễu rời tab và không bật pop-up che màn hình (G10); (2) gỡ kẹt cực ngắn gọn bám đúng mã đoạn bài học; (3) không trả lời chung chung hay lộ đáp án quiz.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3 (`P1`, học tối đều đặn) | 27/11/2026 17:45 | ☑ Đã xong (`P1.md`) |
| Học viên L3 đi làm (`P2`, học tối đều đặn) | 27/11/2026 17:45 | ☑ Đã xong (`P2.md`) |
| Học viên L3 (`P3`, học tối đều đặn) | 27/11/2026 17:46 | ☑ Đã xong (`P3.md`) |
| Học viên L3 (`P4`, học pre-class hiếm khi) | 27/11/2026 17:47 | ☑ Đã xong (`P4.md`) |
