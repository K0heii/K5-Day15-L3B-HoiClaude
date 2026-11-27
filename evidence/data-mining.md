# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script đếm để trong repo: [`evidence/count.py`](count.py) — chỉ dùng thư viện chuẩn Python, người khác chạy `python evidence/count.py <duong-dan-toi-data-preclass>` sẽ ra đúng các số bên dưới.
> Repo chỉ chứa số đã tổng hợp và các dòng ví dụ đã ẩn danh sẵn bởi BTC — **không commit nguyên file data BTC cấp**.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Bộ nhật ký hành vi thật `data/preclass/` do BTC cấp (AI20K khoá 5, Level 3–4), khoảng thời gian `05/11/2026 04:11 UTC → 25/11/2026 09:58 UTC` (21 ngày, Day01 → Day13), gồm `learners.csv` (721 dòng), `events.csv` (107.709 dòng), `answers.csv` (3.776 dòng), `chat.csv` (1.260 dòng), `completed_items.csv` (2.472 dòng), `rewards.csv` (228 dòng).
- **Đếm gì · trên tập nào · lọc gì:**
  1. **Tín hiệu kẹt & bỏ dở khi xem bài (`events.csv`):**
     - Cặp `(hv, video)` có `video_opened` nhưng không có `video_ended`.
     - Lượt `video_seeked` có `to < from` (tua ngược lại) trên tổng số `video_seeked`.
     - Quãng `video_segments_flushed` có `pauses >= 3` (dừng liên tục ≥3 lần trong 1 quãng) và `hidden_count >= 1` (rời tab).
     - Tổng số học viên hoạt động có **≥1 dấu hiệu kẹt rõ**: tua ngược `>= 2` lần HOẶC có quãng dừng `>= 3` lần HOẶC làm sai lần đầu ở `answers.csv`.
  2. **Tỉ lệ làm sai lần đầu (`answers.csv`):**
     - Lọc `lan_thu == 1` và `was_correct in ("True", "False")` (bỏ ô trống không chấm đúng/sai). Đếm `was_correct == False` toàn bộ và riêng các bài có `n >= 20` câu.
     - Đối chiếu số lần đạt thưởng `hanh_vi == "sua_sai"` trong `rewards.csv` so với số câu làm sai lần đầu.
  3. **Hạn chế của AI hiện tại (bị động khi học viên hỏi & xen vào mù quáng khi không lọc tín hiệu):**
     - Trên tập `chat.csv` nối với `answers.csv` (`nguon == "chat"`, đã chấm `rubric_* in {0, 1, 2}`): đếm `rubric_y_moi == 0` (hỏi thụ động không tạo ý mới), `rubric_bam_bai == 0` (lạc đề) và câu hỏi ngắn `do_dai_cau_hoi <= 20` ký tự cùng độ dài phản hồi TB của AI.
     - So sánh số lần bạn học AI chủ động hiện lời (`agent_message_shown` trong `events.csv`) với số lần học viên thực sự trả lời lại lời AI (`la_reply_that == True` trong `answers.csv`).
     - Trên `agent_replied` (`events.csv`): đếm số phản hồi có `moc_trich_dan` rỗng và `missing_context == True`.
  4. **Khung giờ học & tần suất sử dụng (cho Persona §8):**
     - Chuyển `occurred_at` từ UTC sang giờ Việt Nam (`UTC+7`) trên tập sự kiện mở phiên/bài/video (`session_started`, `video_opened`, `lecture_opened`).
     - Đếm số ngày có hoạt động của từng học viên hoạt động trong 21 ngày để phân 3 nhóm dùng ít / vừa / nhiều.
- **Mẫu số là gì:**
  - Khi tính theo **học viên**: mẫu số là **436 học viên có hoạt động** trong `events.csv` (không dùng 721 tài khoản tạo nhưng chưa dùng); riêng tỉ lệ học viên làm sai lần đầu dùng mẫu số **123 học viên có nộp câu hỏi chấm đúng/sai**.
  - Khi tính theo **sự kiện / lượt**: dùng đúng tổng số lượt của chính loại sự kiện đó đã lọc ô trống (vd `N = 3.900` cặp `(hv, video)` mở, `N = 4.322` lượt tua, `N = 22.751` quãng xem, `N = 2.478` lần trả lời đầu có chấm đúng/sai, `N = 1.223` lượt chat đã chấm rubric, `N = 13.975` lần AI bạn học tự xen vào).
- **Script:** `python evidence/count.py <duong-dan-toi-data-preclass>`

## 2. Đọc trước, đếm sau

Đã đọc toàn bộ `README.md`, `column_dictionary.csv` (71 dòng), `event_types.csv` (38 loại sự kiện) và kiểm tra các dòng đầu của `events.csv`, `answers.csv`, `chat.csv`. Các *kiểu* hành vi thấy được trước khi định nghĩa công thức đếm:
- **Kiểu 1 — Gặp câu hỏi / đoạn khó thì bỏ qua hoặc tua ngược ngay lập tức:** nhiều chuỗi sự kiện có học viên đóng bỏ qua câu hỏi giữa video (`quiz_item_dismissed`, `skipped_stop=True`) rồi vài giây sau lập tức tua ngược video (`video_seeked`, `to < from`) để nghe lại đoạn vừa qua.
- **Kiểu 2 — Rời tab xảy ra cực dày đặc (nhiễu rất lớn):** `app_visibility_changed` chiếm tới 30.948 / 107.709 dòng (~28,7% toàn bộ log), cho thấy học viên chuyển tab liên tục (ghi chép, làm việc khác, tra cứu). **Điều này cho thấy rời tab đơn lẻ KHÔNG thể coi là dấu hiệu đọc kẹt** — hệ thống cần phân biệt nhiễu rời tab với tín hiệu kẹt thật.
- **Kiểu 3 — Làm sai liên tiếp ở các bài kỹ thuật nặng nhưng ít sửa sai thành công:** ở Day 06 và Day 13 có học viên làm sai liên tiếp 3 câu trong vài phút, nhưng số lần đạt hành vi `sua_sai` rất thấp.
- **Kiểu 4 — AI xen vào đại trà bị bỏ qua, còn AI hỏi–đáp thì hay trả lời dài không mốc trích dẫn:** `agent_message_shown` bật hàng chục nghìn lần nhưng lượt trả lời lại rất ít; các câu hỏi ngắn 2–6 ký tự lạc đề vẫn nhận đoạn trả lời >130 ký tự và đa số phản hồi không gắn mốc thời gian bài giảng.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Cặp `(hv, video)` mở nhưng **không xem tới cuối** | 2.224 / 3.900 | 57,0% | Chỉ 1.676/3.900 cặp đi tới `video_ended` |
| Lượt tua video là **tua ngược** (`to < from`) | 2.602 / 4.322 | 60,2% | Gặp ở **177 / 436** HV hoạt động (**40,6%**) |
| Quãng xem video **dừng liên tục ≥3 lần** (`pauses >= 3`) | 462 / 22.751 | 2,0% | Gặp ở **100 / 436** HV hoạt động (**22,9%**) |
| Quãng xem video có **rời tab / ẩn app** (`hidden_count >= 1`) | 13.205 / 22.751 | 58,0% | **435 / 436** HV (**99,8%**) có `visible=False` (16.498 lượt) → **bằng chứng rời tab đơn lẻ là nhiễu** |
| **Học viên có ≥1 dấu hiệu kẹt rõ** *(tua ngược ≥2 lần HOẶC dừng ≥3 lần/quãng HOẶC làm sai lần đầu)* | **174 / 436** | **39,9%** | Tần suất tín hiệu kẹt trong 21 ngày: **trung vị 8 lần**, **TB 19,9 lần** (~11,4–28,4 lần/tháng) |
| Câu hỏi **làm sai ngay lần thử đầu** (`lan_thu=1`) | 424 / 2.478 | 17,1% | Gặp ở **73 / 123** HV có làm bài (**59,3%**); riêng **Day 13: 12/29 (41,4%)**, **Day 06: 41/114 (36,0%)**, **Day 05: 55/223 (24,7%)** |
| Lượt được thưởng **sửa sai** (`sua_sai`) / số câu sai lần đầu | 9 / 424 | 2,1% | Rất ít học viên quay lại sửa đúng cùng ý kiến thức sau khi sai |
| Lượt hỏi AI **thụ động không tạo ý mới** (`rubric_y_moi=0`) | 909 / 1.223 | 74,3% | Trên tổng 1.223 lượt chat đã chấm rubric |
| Lượt hỏi AI **lạc đề** (`rubric_bam_bai=0`) | 261 / 1.223 | 21,3% | AI hiện tại vẫn trả lời dài TB **337 ký tự** |
| Câu hỏi **quá ngắn ≤20 ký tự** | 216 / 1.260 | 17,1% | Trong đó **95/216 (44,0%)** lạc đề; AI vẫn trả lời dài TB **270 ký tự** |
| Phản hồi AI **không có mốc trích dẫn** (`moc_trich_dan` rỗng) | 887 / 1.260 | 70,4% | Và **101 / 1.260 (8,0%)** có `missing_context=True` |
| Học viên **trả lời lại** khi AI bạn học tự xen vào (`la_reply_that=True` / `agent_message_shown`) | **91 / 13.975** | **0,65%** | Bật 13.975 lần trên 286 HV nhưng hầu như bị phớt lờ → **bằng chứng thép cần lọc tín hiệu trước khi can thiệp** |
| Sự kiện mở phiên/bài/video vào khung tối–đêm (`18:00–02:00` giờ VN) | 4.337 / 12.631 | 34,3% | Khung `18:00–24:00`: 3.541/12.631 (28,0%); phần còn lại rải rác ban ngày |

**Phân bố tần suất học của 436 học viên hoạt động trong 21 ngày** *(dùng làm nguồn cho Persona chi phí §8)*:
- Dùng ít (1–2 ngày): **216 / 436 (49,5%)**
- Dùng vừa (3–6 ngày): **165 / 436 (37,8%)**
- Dùng nhiều (≥7 ngày): **55 / 436 (12,6%)**

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1. **Bỏ qua câu hỏi giữa video rồi tua ngược ngay 3 giây sau (`events.csv` dòng 195–196):** `L0503` học `program-day01:ai-llm-foundation` (`d01-r1-v01`) lúc `2026-11-05 13:32:44 UTC` (20:32 giờ VN) đóng bỏ qua câu hỏi `day01-ai-llm-foundation:m01:s007` (`skipped_stop=True`), sau đó đúng 3 giây (`13:32:47 UTC`) lập tức tua ngược từ giây `241.3` về `217.5` (−23,8 giây).
2. **Dừng liên tục 3 lần kèm rời tab trong cùng 1 quãng xem (`events.csv` dòng 1979):** `L0010` xem `program-day01:ai-llm-foundation` (`d01-r1-v01`) lúc `2026-11-08 14:10:22 UTC` (21:10 giờ VN) ghi nhận `pauses=3`, `hidden_count=1` trong quãng `343.8s`. Tương tự `L0620` (`events.csv` dòng 15857, `program-day02:ai-problem-definition`, `d02-r2-v02`) có `pauses=3`, `hidden_count=1` trong `192.4s`.
3. **Tua ngược đoạn dài khi học tối (`events.csv` dòng 73 & 303):** `L0006` tua ngược gần 50 giây (`88.9s → 40.8s`) trên `d01-r1-v01` lúc `17:55` VN; `L0424` tua ngược 30,7 giây (`133.0s → 102.3s`) trên `d01-r1-v02` lúc `20:54` VN.
4. **Làm sai liên tiếp 3 câu lần đầu trong 3 phút ở bài kỹ thuật nặng (`answers.csv` mã `A00161`, `A00883`, `A01376`):** `L0597` làm `program-day06:data-engineering-for-agents` (`pre_post_post`) lúc `2026-11-12 11:44–11:47 UTC` (18:44–18:47 VN) sai liên tiếp 3 ý kiến thức (`more_data_amplifies_stale_copies`, `raw_clean_serve_layers`, `batch_rules_beyond_schema`).
5. **Câu hỏi quá ngắn, lạc đề nhưng AI vẫn trả lời dài không làm rõ (`chat.csv` mã `C01056`, `C00048`):** `L0057` nhắn đúng **2 ký tự** ở `Day01/d01-r1-v01.txt` (`rubric_bam_bai=0`, `rubric_y_moi=0`) nhưng AI vẫn sinh câu trả lời **171 ký tự**; `L0663` nhắn **6 ký tự** (`bam_bai=0`) vẫn nhận câu trả lời **131 ký tự**.
6. **AI trả lời khi thiếu ngữ cảnh và không có mốc trích dẫn (`events.csv` dòng 112):** `L0213` nhận `agent_replied` mã `C00983` lúc `2026-11-05 12:56:39 UTC` (19:56 VN) với `missing_context=True` và `moc_trich_dan` rỗng.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**:
- **Không có nội dung chữ học viên gõ** (chỉ có số ký tự và điểm rubric) → không biết chính xác câu hỏi cụ thể hay lý do thực sự học viên rời tab (tra cứu ChatGPT/Google, ghi chép Notion, hay làm việc cá nhân).
- **Khoảng thời gian chỉ 21 ngày (`05/11–25/11/2026`) và thiếu hoạt động của 285/721 tài khoản** → các bài cuối (như Day 13, `n = 29` câu) có cỡ mẫu nhỏ hơn các bài đầu (Day 01–05).
- **Dữ liệu không phân biệt thời gian dừng để ghi chép vs dừng do kẹt kiến thức.**

→ **Kiểm lại bằng phỏng vấn:** nhóm phỏng vấn trực tiếp **4 học viên L3 ngoài nhóm** (`evidence/interviews/P1.md` – `P4.md`, chiều Thứ Sáu 27/11/2026) để xác nhận *vì sao* họ dừng/tua/chuyển tab, mỗi lần kẹt tốn bao nhiêu phút thật, và khi nào gợi ý AI bị coi là làm phiền.
