# AI SPEC — Adaptive Pre-class Scaffolding · Nhóm HoiClaude · Lớp L3B

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: Adaptive Pre-class Scaffolding (gỡ kẹt chủ động theo tín hiệu quá tải nhận thức khi học pre-class AI20K, mở rộng từ nhóm bài toán A1 học tập pre-class)
Data BTC cấp đã dùng (nếu có — không commit nguyên file): `data/preclass/` (`answers.csv`, `chat.csv`, `events.csv`, `learners.csv`, `completed_items.csv`)

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin):
  1. Học viên đăng nhập `preclass-online.com` buổi tối trước buổi học để xem video/đọc bài pre-class.
  2. Gặp đoạn kiến thức kỹ thuật nặng → dừng video, tua đi tua lại hoặc làm sai câu hỏi kiểm tra giữa bài.
  3. Khi vẫn chưa hiểu, học viên phải tự diễn đạt câu hỏi gõ vào ô chat trợ giảng AI (hoặc mở tab mới hỏi ChatGPT / Google), dễ nhận câu trả lời dài không gắn đúng đoạn bài hoặc bị phân tâm khỏi trang học.
  4. Nhiều trường hợp học viên bỏ qua đoạn khó, bấm qua bài để kịp tiến độ mà chưa thực sự hiểu trước giờ lên lớp.
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm": Trợ giảng AI và bạn học AI tích hợp sẵn trên `preclass-online.com` (dạng hỏi–đáp bị động, nguồn: mô tả Track A & nhật ký `data/preclass/chat.csv`) + học viên tự mở ChatGPT/Google bên ngoài (sẽ kiểm chứng qua phỏng vấn).

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): Học viên AI20K K5 (khối L3) tự học bài pre-class buổi tối sau giờ làm/học, gặp đoạn kiến thức kỹ thuật nặng trước giờ lên lớp.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): Hiểu đúng ý cốt lõi của đoạn kiến thức kỹ thuật khó ngay trong lúc tự học bài pre-class buổi tối để trả lời đúng câu kiểm tra và kịp chuẩn bị trước giờ lên lớp.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ:
  - *Cách đang làm:* Tua đi tua lại video/đoạn bài, gõ câu hỏi ngắn vào chat dưới bài, hoặc mở tab mới tra Google/ChatGPT.
  - *Hỏng ở đâu:* Khi đang quá tải nhận thức, học viên khó diễn đạt đúng chỗ kẹt (hỏi quá ngắn/lệch ý), còn việc mở tab ngoài làm đứt mạch tập trung; đọc tóm tắt dài không gắn đoạn bài dẫn tới học thụ động.
  - *Vì sao chưa bỏ:* Đây là cách duy nhất có sẵn ngay lúc tự học tối muộn khi không có giảng viên/TA trực tiếp bên cạnh.
- Pain (KHÔNG chữ AI): Học viên L3 tự học bài pre-class buổi tối khi gặp đoạn kiến thức kỹ thuật khó thường dừng lâu, tua lại nhiều lần hoặc làm sai câu kiểm tra rồi phải chuyển tab tự tra cứu bên ngoài, làm đứt mạch tập trung và dẫn tới học thụ động hoặc bỏ dở bài trước giờ lên lớp.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): *(Đang hoàn thiện CP2–CP3)* Khám phá bước đầu trên `data/preclass/` cho thấy 424/2.478 câu làm sai ở lần thử đầu (17,1%; cao tới 36,0% ở Day 06 và 41,4% ở Day 13) và 909/1.223 lượt chat đã chấm (74,3%) có `rubric_y_moi = 0`. Nhóm sẽ hoàn thiện script đào `events.csv` + phỏng vấn ≥4 học viên ngoài nhóm chiều T6 27/11.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"):
  - **Nguyễn Như Duy An (`2A202603783` · Đội trưởng):** Điều phối, nộp 4 checkpoint, đào bằng chứng `evidence/` & phỏng vấn, bảng Impact (`spec.md` §1–§2), tổng hợp slide `demo-slides.pdf`.
  - **Nguyễn Minh Quang (`2A202603791`):** Thiết kế kiến trúc (`spec.md` §4), `data/DATA_CARD.md`, xây dựng lõi `codebase/` (`agent.py`, `tools.py`, `ai.py`).
  - **Đào Văn Hiệp (`2A202603813`):** Bộ câu thử `eval/benchmark.csv`, metric & chuẩn "đạt" (`eval/metric_spec.yaml`, `spec.md` §5–§7), chạy & báo cáo đánh giá lượt 1–2 (`eval/report.md`).
  - **Lã Thái Minh (`2A202603756`):** Mô phỏng chi phí (`cost/`), phỏng vấn & thử nghiệm người dùng (`validation/log.md`), hỗ trợ slide & video demo dự phòng.
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`): Nhóm dùng trợ lý coding AI để hỗ trợ khám phá cấu trúc repo, rà soát format tài liệu và sinh khung mã nguồn/script phân tích; toàn bộ quyết định chọn lát cắt, kiểm chứng số liệu thật, chấm điểm câu thử và giải thích kiến trúc đều do thành viên trực tiếp duyệt và chịu trách nhiệm.
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
