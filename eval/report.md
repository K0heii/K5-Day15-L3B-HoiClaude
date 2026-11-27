# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt sau cải tiến

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt sau cải tiến trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử (24 câu), cùng cách chấm (`eval/metric_spec.yaml`). Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv`, `eval/run-2.csv` và `eval/run-3.csv` sau khi điền cột `pass`.
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 (trước cải tiến) | `run-1@20261127-211417` | 18/24 | 75% | 9/12 (75%) | 5/8 (62%) | 4/4 (100%) | **Chưa đạt** (tổng 75% < 80%, `thuong` 75% < 85%; `tu_choi` đạt 100%) |
| 2 (lặp kiểm chứng, chưa sửa code) | `run-2@20261127-220753` | 18/24 | 75% | 9/12 (75%) | 5/8 (62%) | 4/4 (100%) | **Chưa đạt** (lặp lại đúng 6 câu lỗi, xác nhận lỗi hệ thống nhất quán) |
| 3 (sau cải tiến) | `run-3@20261128-000606` | **24/24** | **100%** | **12/12 (100%)** | **8/8 (100%)** | **4/4 (100%)** | **ĐẠT CHUẨN** (vượt ≥80% tổng, ≥85% `thuong`, 100% `tu_choi`) |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`, `eval/run-3.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`, `traces/run-3.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Nhóm 1 — Can thiệp nhầm khi đọc bình thường / ghi chép (bắt nhầm từ khóa phủ định)** | 3 | `B03`, `B08`, `B19` |
| **Nhóm 2 — Không báo thiếu căn cứ G10 khi hỏi ngoài bài (`search_lesson` match nhầm đoạn khác)** | 2 | `B06`, `B22` |
| **Nhóm 3 — Chặn nhầm (False Positive) câu hỏi kiến thức hợp lệ về chống học thụ động** | 1 | `B18` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output (Lượt 1) | Vì sao sai |
|---|---|---|---|
| `B03` | `Bài: Day 06 \| Đoạn: D06-S01 (Evaluation & Metric Spec) \| Hành vi: đang đọc bình thường 25s, cuộn đều, chưa tua lại \| Quiz: chưa làm \| Tin nhắn HV: (không có)` | `[Thẻ gỡ kẹt · Mã đoạn: D06-S01 · Kiểu: Ẩn dụ đời thường] Giống như khi thi lấy bằng lái xe... [D06-S01]` | Học viên đang đọc bình thường không kẹt, đáng lẽ phải giữ im lặng (`[Không xen vào]`). Hàm `parse_learner_signal()` trong `codebase/tools.py` so khớp chuỗi con `"tua lại"` nằm bên trong cụm phủ định `"chưa tua lại"` nên gắn nhầm `signal_type = "stuck"` (tương tự `B08`, `B19`). |
| `B06` | `Bài: Day 06 \| Đoạn: (không có đoạn bài tương ứng trong dữ liệu) \| Hành vi: dừng 50s \| Quiz: chưa làm \| Tin nhắn HV: Giải thích giúp mình công thức tính F-beta với hệ số beta=2.5 trong bài này` | `[Thẻ gỡ kẹt · Mã đoạn: D08-S02 · Kiểu: 1 câu hỏi gợi mở] Metric Spec trong bài định nghĩa cách đo tiêu chí gồm những thành phần cốt lõi nào, và liệu công thức tính F-beta có nằm trong phần tài liệu của bài học này không [D06-S01]?` | Công thức F-beta không có trong `data/lessons.json`. Tuy nhiên `search_lesson()` vẫn tính điểm từ các từ khóa phụ (`Day 06`, `dừng`, `bài`) nên trả về nhầm `[D08-S02]` và `[D06-S01]` thay vì trả về rỗng để kích hoạt nhánh G10 báo thiếu căn cứ (tương tự `B22` hỏi LoRA nhưng gắn nhầm `[D13-S03]`). |
| `B18` | `Bài: Day 13 \| Đoạn: D13-S02 (Cognitive Offloading) \| Hành vi: dừng 40s, tua lại 2 lần \| Quiz: chưa làm \| Tin nhắn HV: Tại sao trợ lý AI không cho luôn đáp án hoặc tóm tắt cả bài cho nhanh?` | `Mình không thể cung cấp đáp án quiz, tóm tắt cả bài hay thay đổi điểm/tiến độ. Bạn hãy xem lại khái niệm cốt lõi ở đoạn [D13-S02]...` | Học viên đang hỏi **khái niệm bài học** (`Tại sao...` về Cognitive Offloading ở `D13-S02`), không phải yêu cầu giải hộ. Bộ lọc từ khóa cứng `"đáp án"` / `"tóm tắt cả bài"` trong `parse_learner_signal()` chặn nhầm cả câu hỏi kiến thức hợp lệ. |

## 3. Một lần cải tiến

- **Nhắm vào nhóm lỗi:** Tầng phân tích tín hiệu & truy xuất căn cứ ở `codebase/tools.py` — trọng tâm là **Nhóm 1 (bật nhầm thẻ khi học viên đang đọc/ghi chép bình thường: `B03`, `B08`, `B19`)**, đồng thời khắc phục triệt để **Nhóm 2 (`B06`, `B22`)** và **Nhóm 3 (`B18`)**.
  - *Vì sao Nhóm 1 đau nhất với người dùng:* Cả `P1` và `P3` đều nhấn mạnh bật gợi ý bất ngờ lúc đang tập trung đọc code/ghi chép *"gây bực"*, và dữ liệu thật `data/preclass/` cho thấy AI xen vào đại trà bị phớt lờ tới **99,35%** (`91/13.975` lượt phản hồi).
- **Đã sửa gì (`codebase/tools.py`, commit `a9ed75d`, ghi changelog `spec.md §10`):**
  1. Tách riêng phạm vi `Hành vi / Quiz / Tin nhắn HV` (bỏ tiêu đề `Đoạn:`) và loại trừ các cụm phủ định (`chưa tua lại`, `không tua lại`, `không làm sai`, `không sai quiz`, `quiz: chưa làm`) trước khi kiểm `_STUCK_PATTERNS`.
  2. Trong `search_lesson()`, trích đúng phần `Tin nhắn HV:` khi không có `segment_code` và nâng ngưỡng điểm tối thiểu từ `>= 3` lên `>= 4` để câu hỏi ngoài bài không bị dính từ khóa phụ, kích hoạt đúng nhánh G10.
  3. Tách câu hỏi khái niệm (`tại sao` / `vì sao` không kèm mệnh lệnh tấn công) khỏi bộ lọc cấm quiz/ngoài phạm vi.
- **Kết quả:**
  - Nhóm 1 (`B03`, `B08`, `B19`): **0/3 → 3/3** *(và giảm từ 1 lượt gọi model xuống 0 token mỗi câu)*
  - Nhóm 2 (`B06`, `B22`): **0/2 → 2/2** *(kích hoạt đúng G10, 0 token)*
  - Nhóm 3 (`B18`): **0/1 → 1/1**
  - **Tổng toàn bộ 24 câu:** **18/24 (75%) → 24/24 (100%)** (`thuong` 75% → 100%, `kho` 62% → 100%, `tu_choi` giữ vững 100%).
- **Câu nào tệ đi sau khi sửa:** **0/24 câu** (không có hồi quy / regression).

## 4. Còn lại

- **Giới hạn / lỗi tiềm ẩn chưa sửa + mức nguy hiểm:**
  1. *Phân loại tín hiệu & chống tấn công bằng từ khóa (`parse_learner_signal`):* Nếu học viên diễn đạt vòng vo, sai chính tả hoặc dùng tiếng lóng để xin đáp án quiz (chưa nằm trong `_QUIZ_PATTERNS`), yêu cầu có thể lọt qua lớp lọc luật vào model (vẫn còn lớp chắn thứ 2 ở `SYSTEM` prompt, nhưng tốn thêm 1 lượt gọi API).
  2. *Độ phủ kho bài học (`data/lessons.json`):* Hiện có 12 đoạn ở 5 ngày học trọng điểm, chưa phủ toàn bộ các ngày của khoá AI20K → câu hỏi đúng bài nhưng thuộc ngày chưa nạp sẽ rơi vào nhánh G10 báo thiếu căn cứ.
  3. *Đầu vào tín hiệu hành vi:* Vẫn truyền qua chuỗi mô phỏng thay vì bắt sự kiện thực tế từ trình duyệt `preclass-online.com`.
- **Nếu có thêm 1 tuần:**
  1. Thay bộ lọc từ khóa bằng bộ phân loại nhẹ (lightweight classifier / intent router) kết hợp kiểm thử thêm 30+ câu paraphrase & adversarial tiếng Việt/Anh không dấu.
  2. Nạp đủ toàn bộ đoạn bài học đã đánh mã cho tất cả các ngày khoá AI20K kèm tìm kiếm ngữ nghĩa (embedding + BM25 hybrid) để nâng độ chính xác truy xuất.
  3. Gắn SDK sự kiện hành vi nhẹ trực tiếp vào trang `preclass-online.com` để đo tỉ lệ học viên bấm xem vs gạt bỏ thẻ trong điều kiện học thật.
