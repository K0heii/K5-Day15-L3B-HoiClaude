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
- **Chatbot trợ giảng bị động dưới bài trên `preclass-online.com`:** Đáng học ở chỗ đặt ngay cạnh bài học, không cần chuyển trang · Đáng né ở chỗ chỉ chờ học viên tự nghĩ ra câu hỏi và trả lời dài dạng văn bản · Mình khác ở chỗ đọc tín hiệu kẹt để gợi ý chủ động đúng 1 kiểu gỡ kẹt ngắn gọn gắn mã đoạn.
- **Mở tab ngoài hỏi ChatGPT / Gemini / Google:** Đáng học ở chỗ giải thích linh hoạt bằng ví dụ đời thường · Đáng né ở chỗ làm đứt mạch tập trung, dễ bịa ngoài phạm vi bài học và dễ dẫn tới hỏi hộ đáp án quiz · Mình khác ở chỗ khóa chặt căn cứ vào `data/lessons.json` (`[DXX-SYY]`) và chặn 100% lộ đáp án quiz.
- **Extension giám sát webcam / theo dõi chuyển động mắt:** Đáng học ở chỗ phát hiện sớm sự mất tập trung · Đáng né ở chỗ xâm phạm quyền riêng tư, nặng về cài đặt kỹ thuật và dễ báo nhầm khi học viên chỉ nhìn xuống ghi chép · Mình khác ở chỗ dùng tín hiệu hành vi học tập thuần (tua lại, dừng lâu tại đoạn, sai quiz) và luôn cho phép gạt bỏ ngay.

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): Một học viên L3 đang học bài pre-class gặp dấu hiệu kẹt ở một đoạn kiến thức (dừng lâu / tua lại nhiều lần / vừa làm sai câu kiểm tra) · cần hiểu đúng ý cốt lõi ngay tại đoạn đó mà không đứt mạch · AI đọc ngữ cảnh đoạn bài + tín hiệu hành vi để quyết định **không xen vào** hay **can thiệp đúng 1 kiểu gỡ kẹt** (ẩn dụ đời thường / sơ đồ Mermaid ngắn / 1 câu hỏi gợi mở, bắt buộc kèm mã đoạn bài, không lộ đáp án) · học viên hiểu nhanh ý cốt lõi, kiểm chứng ngay tại đoạn bài và tự trả lời được câu kiểm tra.
- **Không làm (≥3 điều):**
  1. Không dùng webcam, micro hay cài browser extension theo dõi thiết bị cá nhân.
  2. Không giải hộ, gợi ý trực tiếp đáp án A/B/C/D của quiz hay tự động chấm/sửa điểm.
  3. Không tóm tắt trọn vẹn cả bài học hoặc bịa thêm kiến thức nằm ngoài đoạn bài trong `data/lessons.json`.
  4. Không tự ý gửi tin nhắn ra ngoài hoặc thay đổi tiến độ học của học viên.
- **Sơ đồ kiến trúc:**
```mermaid
flowchart TD
    A["Đầu vào: Ngữ cảnh đoạn bài + Tín hiệu hành vi / Câu hỏi"] --> B["Bước 1: parse_learner_signal()"]
    B --> C{"Xin đáp án quiz hoặc ngoài phạm vi?"}
    C -- Có --> D["Từ chối an toàn (0% lộ đáp án) + nhắc đoạn bài"]
    C -- Không --> E{"Tín hiệu là rời tab / đọc bình thường?"}
    E -- Có --> F["Không xen vào (giữ nguyên mạch học)"]
    E -- Không (kẹt rõ ràng) --> G["Bước 2: search_lesson() tra data/lessons.json"]
    G --> H{"Có đoạn bài khớp?"}
    H -- Không --> I["G10: Thu hẹp phạm vi — báo thiếu căn cứ, không bịa"]
    H -- Có --> J["Bước 3: call_model() chọn đúng 1 kiểu gỡ kẹt + trích mã [DXX-SYY]"]
    J --> K["Bước 4: draft_scaffolding_card() tạo thẻ nháp bên lề"]
    K --> L["Học viên tự đọc, đối chiếu đoạn bài hoặc gạt bỏ"]
```
- **Hình dạng:** `[x] workflow cố định` · [ ] một agent · [ ] nhiều agent — Luồng xử lý gồm 4 bước tuần tự rõ ràng (lọc tín hiệu → tra căn cứ → gọi AI chọn 1 kiểu gỡ kẹt → đóng gói thẻ nháp), dễ kiểm soát chi phí token và hành vi an toàn. Không chọn vòng lặp agent tự chủ hay nhiều agent vì không cần AI tự quyết định thêm bước gọi tool, tránh rủi ro lặp vô hạn và tăng độ trễ khi học viên đang học.
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | `parse_learner_signal(text)` | Chuỗi đầu vào gồm câu hỏi và/hoặc tín hiệu hành vi (`str`) | `dict` gồm `signal_type`, `segment_code`, `is_quiz_answer_request`, `is_out_of_scope`, `query` | Không |
  | `search_lesson(query, segment_code)` | Từ khoá tìm kiếm (`str`) và mã đoạn tuỳ chọn (`str`) | Danh sách tối đa 3 đoạn bài khớp `{"code", "day", "topic", "title", "content", "common_trap"}` | Không |
  | `draft_scaffolding_card(segment_code, mode, body)` | Mã đoạn (`str`), kiểu gỡ kẹt (`str`), nội dung thẻ (`str`) | `dict` bản nháp thẻ gợi ý `{"status", "segment_code", "mode", "card_text"}` | Không (chỉ tạo bản nháp hiển thị tại chỗ, học viên tự xem/gạt bỏ) |

- **Mức tự động:** `[x] AI gợi ý, người quyết` · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — Nếu AI báo nhầm lúc học viên không kẹt sẽ gây phiền và đứt mạch; nếu AI hiểu sai ý sẽ làm học viên hiểu lệch kiến thức, nên thẻ gợi ý phải hiển thị ở dạng bản nháp nhẹ bên lề để học viên tự quyết định đọc hay gạt bỏ ngay.
- **Chỗ chặn rủi ro:**
  1. Cổng lọc đầu vào ở `parse_learner_signal` chặn ngay yêu cầu xin đáp án quiz / tóm tắt cả bài / sửa điểm trước khi gọi model.
  2. `SYSTEM` prompt + kiểm tra đầu ra ở `agent.py` ép buộc chỉ chọn 1 kiểu gỡ kẹt dựa trên đoạn bài trả về từ `search_lesson`, kèm mã `[DXX-SYY]`.
- **Chỗ người duyệt:** Học viên tự quyết định chấp nhận đọc, đối chiếu lại đoạn bài hoặc bấm gạt bỏ thẻ gợi ý; AI tuyệt đối không tự nộp bài quiz, không tự sửa điểm hay đánh dấu hoàn thành bài học.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Nhánh `Không có đoạn bài khớp` sau `search_lesson()` trong `agent.py` dừng ngay, báo thiếu căn cứ thay vì gọi model tự bịa; nhánh `rời tab / đọc bình thường` chọn không xen vào. |
  | Grounding bắt buộc kèm mã nguồn | `search_lesson()` luôn trả về `code` (`DXX-SYY`) và `agent.py` yêu cầu thẻ gợi ý gắn mã đoạn để học viên kiểm chứng tại chỗ. |
  | Chống học thụ động (0% lộ đáp án) | Cổng `is_quiz_answer_request` ở `parse_learner_signal()` và ràng buộc `SYSTEM` prompt cấm nêu đáp án đúng/sai hoặc tóm tắt trọn bài. |

- **Phần nào còn giả (ghi rõ ở mốc CP2):**
  1. Ở cấu hình mặc định chưa điền `.env`, `codebase/ai.py` chạy chế độ giả (`MODEL_PROVIDER=fake`, token = 0) để đi hết luồng trước CP2; sẽ nối model thật ở CP3.
  2. Tín hiệu hành vi (dừng lâu, tua lại, rời tab, sai quiz) được truyền qua chuỗi text mô phỏng trong `input` thay vì đọc trực tiếp từ trình duyệt `preclass-online.com`.
  3. Kho bài học `data/lessons.json` gồm 12 đoạn viết lại/rút gọn ở 5 chủ điểm tiêu biểu, chưa bao phủ toàn bộ các ngày của khoá AI20K.

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
