# Chi phí khi dùng thật — CP4

## 1. Đầu vào và giả định

- [cost/personas.yaml](./personas.yaml) đặt 3 kiểu học viên: học ít (49,54%, 2,5 phiên/người/tháng, 1 lượt hỏi/phiên), học vừa (37,84%, 7 phiên, 2 lượt hỏi), học nhiều (12,61%, 14 phiên, 2 lượt hỏi). Tỷ trọng lấy từ số ngày hoạt động của 436 học viên ở [evidence/data-mining.md](../evidence/data-mining.md) §3; tần suất phiên và lượt hỏi là **tự ước tính**, chưa đo trên hệ thống học thật. Mô phỏng dùng 50 phiên, seed 42.
- Quy mô thấp/cơ sở/cao: 300/700/1.000 người dùng mỗi tháng. 700 học viên L3 và khoảng 1.000 học viên cả khóa theo nguồn nêu ở [spec.md](../spec.md) §2; mức thấp 300 là **tự ước tính**. Đây là kịch bản quy mô, chưa phải số người dùng cam kết.
- Giá API trả phí ghi trong [cost/personas.yaml](./personas.yaml), tra từ [bảng giá Google AI Studio](https://aistudio.google.com/docs/pricing) ngày 27/11/2026: Gemini 3.5 Flash-Lite 0,30 USD/triệu token vào và 2,50 USD/triệu token ra; Gemini 4 Hydrogen 1,50 và 7,50 USD/triệu token. Cần kiểm tra lại giá trước khi triển khai.
- Tỷ lệ đạt đầu vào là **24/24 (100%)** ở [eval/run-3.csv](../eval/run-3.csv), run ID `run-3@20261128-000606`, theo chuẩn đã chốt ở [spec.md](../spec.md) §7. Đây là bộ câu thử cố định, không phải tỷ lệ thành công ngoài thực tế.
- Token được đo khi gọi Gemini 3.5 Flash-Lite; chi phí Gemini 4 Hydrogen là phép tính theo bảng giá với cùng lượng token, nên chỉ là kịch bản so sánh. Tokenizer hoặc đầu ra model khác có thể làm chi phí thực tế khác đi.

## 2. Kết quả mô phỏng

Lượt dùng để ước tính: [cost/simulate-2.csv](./simulate-2.csv), run ID `simulate-2@20261128-002614`; **50/50 phiên không lỗi** (học ít 23, học vừa 24, học nhiều 3). Bảng dưới chép từ [cost/simulate-2-summary.md](./simulate-2-summary.md).

| Model | USD/phiên | USD/task đạt | USD/câu hỏi đạt | 300 người/tháng | 700 người/tháng | 1.000 người/tháng | USD/người/tháng, cơ sở |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash-Lite | 0,00037 | 0,00037 | 0,00024 | 0,7306 | 1,70 | 2,44 | 0,0024 |
| Gemini 4 Hydrogen | 0,0014 | 0,0014 | 0,00093 | 2,79 | 6,51 | 9,30 | 0,0093 |

Chi phí/task đạt = chi phí trung bình/phiên ÷ tỷ lệ đạt. Vì bộ câu thử hiện đạt 100%, hai cột bằng nhau; **không giả định 100% khi dùng thật**. Nếu tỷ lệ đạt chỉ 75%, chi phí/task đạt xấp xỉ 0,00049 USD (Flash-Lite) hoặc 0,0019 USD (Hydrogen), với giả định chi phí/phiên giữ nguyên.

[cost/simulate-1.csv](./simulate-1.csv) là lượt thử trước đó: 28/50 phiên gặp HTTP 429 do hạn mức gọi API, nên **không dùng để tính chi phí**. Lượt 2 thêm thời gian chờ giữa các lệnh gọi và hoàn tất 50/50 phiên. Hạn mức API vẫn là rủi ro vận hành cần kiểm tra với tải thật.

## 3. So với impact và quyết định

[spec.md](../spec.md) §2 ước tính 280 học viên bị kẹt, mỗi người 2 lần/tháng, mỗi lần 15 phút: **8.400 phút (140 giờ)/tháng có thể tác động**. Đây là cơ hội cải thiện **tự ước tính**, chưa phải thời gian đã tiết kiệm được. Ở quy mô cơ sở 700 người dùng, chi phí API khoảng **1,70 USD/tháng** với Flash-Lite hoặc **6,51 USD/tháng** theo kịch bản giá Hydrogen.

**Kết luận:** đáng thử thí điểm có đo lường vì chi phí API mô phỏng thấp; chưa đủ dữ liệu để khẳng định hiệu quả học tập hay quyết định triển khai rộng. Cần đo việc học viên có đọc, hiểu và sử dụng thẻ gợi ý đúng lúc hay không, cùng lỗi và chi phí khi có tải thật. Bảng này chưa gồm hosting, lưu trữ, giám sát và công người duyệt.
