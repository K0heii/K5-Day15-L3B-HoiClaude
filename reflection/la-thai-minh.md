# Reflection — Lã Thái Minh

> Nhóm HoiClaude · Lớp L3B · Mã học viên: `2A202603756`.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**  
   Mình phỏng vấn học viên P2 ([ghi chép](../evidence/interviews/P2.md)), chấm chéo 5 mẫu với Hiệp ([phiếu chấm](../eval/cross-grade-5-samples.md)) và hỗ trợ chấm các lượt eval.  
   Ở CP4, mình chuẩn bị giả định trong [personas.yaml](../cost/personas.yaml), chạy mô phỏng 50 phiên và viết cách tính, giới hạn trong [cost-estimate.md](../cost/cost-estimate.md), [spec.md](../spec.md) §8–§9.  
   Mình hỗ trợ [slide demo](../demo-slides.pdf), chuẩn bị kịch bản dùng thử trong [log.md](../validation/log.md); phần CP4 đã lên `main` ở commit `0a3010d`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**  
   Mình dùng Codex để đọc repo, soạn nháp báo cáo chi phí, phần rủi ro và dàn 8 slide từ số liệu có nguồn.  
   Bản nháp AI từng ghi nhầm run ID của `simulate-2` và coi cả tỷ trọng persona là tự ước tính; các chỗ này đã được sửa theo [summary](../cost/simulate-2-summary.md) và [data-mining.md](../evidence/data-mining.md). Lượt `simulate-1` có 28/50 phiên lỗi HTTP 429 nên phải chạy lại và loại khỏi ước tính.  
   AI chỉ chuẩn bị kịch bản dùng thử; [log.md](../validation/log.md) chưa có quan sát hoặc trích dẫn người thử thật để điền thay.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**  
   Ở lượt 1, câu `B08` trượt: học viên dừng 55 giây để ghi chép, không tua lại và không sai quiz, nhưng hệ thống vẫn bật thẻ gợi ý ([report.md](../eval/report.md)).  
   Bộ lọc bắt nhầm từ khóa nằm trong cụm phủ định, nên một tín hiệu học bình thường bị hiểu thành đang kẹt. Mình học được rằng trợ lý chủ động phải xét **ngữ cảnh phủ định và quyền được yên của người học**.  
   Sau khi nhóm sửa tầng phân tích tín hiệu, lượt 3 đạt 24/24; kết quả này vẫn cần kiểm tra với câu lạ và người dùng thật trước khi kết luận sản phẩm hữu ích ngoài bài thử.
