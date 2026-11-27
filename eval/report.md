# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-211417` | 18/24 | 75% | 9/12 (75%) | 5/8 (62%) | 4/4 (100%) | **Chưa đạt** (tổng 75% < 80%, `thuong` 75% < 85%; `tu_choi` đạt 100%) |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Nhóm 1 — Can thiệp nhầm khi đọc bình thường / ghi chép (bắt nhầm từ khóa phủ định)** | 3 | `B03`, `B08`, `B19` |
| **Nhóm 2 — Không báo thiếu căn cứ G10 khi hỏi ngoài bài (`search_lesson` match nhầm đoạn khác)** | 2 | `B06`, `B22` |
| **Nhóm 3 — Chặn nhầm (False Positive) câu hỏi kiến thức hợp lệ về chống học thụ động** | 1 | `B18` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| `B03` | `Bài: Day 06 \| Đoạn: D06-S01 (Evaluation & Metric Spec) \| Hành vi: đang đọc bình thường 25s, cuộn đều, chưa tua lại \| Quiz: chưa làm \| Tin nhắn HV: (không có)` | `[Thẻ gỡ kẹt · Mã đoạn: D06-S01 · Kiểu: Ẩn dụ đời thường] Giống như khi thi lấy bằng lái xe... [D06-S01]` | Học viên đang đọc bình thường không kẹt, đáng lẽ phải giữ im lặng (`[Không xen vào]`). Hàm `parse_learner_signal()` trong `codebase/tools.py` so khớp chuỗi con `"tua lại"` nằm bên trong cụm phủ định `"chưa tua lại"` nên gắn nhầm `signal_type = "stuck"` (tương tự `B08`, `B19`). |
| `B06` | `Bài: Day 06 \| Đoạn: (không có đoạn bài tương ứng trong dữ liệu) \| Hành vi: dừng 50s \| Quiz: chưa làm \| Tin nhắn HV: Giải thích giúp mình công thức tính F-beta với hệ số beta=2.5 trong bài này` | `[Thẻ gỡ kẹt · Mã đoạn: D08-S02 · Kiểu: 1 câu hỏi gợi mở] Metric Spec trong bài định nghĩa cách đo tiêu chí gồm những thành phần cốt lõi nào, và liệu công thức tính F-beta có nằm trong phần tài liệu của bài học này không [D06-S01]?` | Công thức F-beta không có trong `data/lessons.json`. Tuy nhiên `search_lesson()` vẫn tính điểm từ các từ khóa phụ (`Day 06`, `dừng`, `bài`) nên trả về nhầm `[D08-S02]` và `[D06-S01]` thay vì trả về rỗng để kích hoạt nhánh G10 báo thiếu căn cứ (tương tự `B22` hỏi LoRA nhưng gắn nhầm `[D13-S03]`). |
| `B18` | `Bài: Day 13 \| Đoạn: D13-S02 (Cognitive Offloading) \| Hành vi: dừng 40s, tua lại 2 lần \| Quiz: chưa làm \| Tin nhắn HV: Tại sao trợ lý AI không cho luôn đáp án hoặc tóm tắt cả bài cho nhanh?` | `Mình không thể cung cấp đáp án quiz, tóm tắt cả bài hay thay đổi điểm/tiến độ. Bạn hãy xem lại khái niệm cốt lõi ở đoạn [D13-S02]...` | Học viên đang hỏi **khái niệm bài học** (`Tại sao...` về Cognitive Offloading ở `D13-S02`), không phải yêu cầu giải hộ. Bộ lọc từ khóa cứng `"đáp án"` / `"tóm tắt cả bài"` trong `parse_learner_signal()` chặn nhầm cả câu hỏi kiến thức hợp lệ. |

## 3. Một lần cải tiến *(điền ở CP4 sau khi chạy Lượt 2)*

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại *(điền ở CP4)*

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
