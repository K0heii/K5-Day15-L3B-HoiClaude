# Kế hoạch chia việc — Nhóm HoiClaude (L3B · Track A)

> **Lát cắt:** **Adaptive Pre-class Scaffolding** — Trợ lý gỡ kẹt chủ động theo tín hiệu quá tải nhận thức khi học pre-class AI20K (gọt bỏ Webcam/Extension, chạy lõi Python chuẩn khung `starter-repo`).
> **Repo nhóm:** https://github.com/K0heii/K5-Day15-L3B-HoiClaude

---

## 1. Phân vai & Quyền sở hữu file *(tránh đụng Git conflict)*

| Thành viên | Mã HV | Vai trò | File được phép sửa trực tiếp |
|---|---|---|---|
| **Nguyễn Như Duy An** | `2A202603783` | **Đội trưởng** · Điều phối, nộp CP1–CP4, Evidence, Impact, Slide | `TEAMS.md`, `canvas.md`, `evidence/data-mining.md`, `evidence/summary.md`, `evidence/interviews/P1.md`, `spec.md` (§0–§2, §10), `slides/outline.md`, `demo-slides.pdf` |
| **Nguyễn Minh Quang** | `2A202603791` | Kiến trúc AI · Data bài học · Lõi `codebase/` | `spec.md` (§3–§4), `data/` (`DATA_CARD.md`, dữ liệu đoạn bài học), `codebase/` (`agent.py`, `tools.py`, `ai.py`), `README.md` |
| **Đào Văn Hiệp** | `2A202603813` | Benchmark · Metric & Chuẩn đạt · Eval lượt 1–2 | `spec.md` (§5–§7), `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/report.md`, `eval/README.md`, `evidence/interviews/P3.md` |
| **Lã Thái Minh** | `2A202603756` | Mô phỏng chi phí · Phỏng vấn & User Test (+5đ) · Video demo | `cost/personas.yaml`, `cost/cost-estimate.md`, `spec.md` (§8–§9), `validation/log.md`, `evidence/interviews/P2.md`, `P4.md`, quay video demo |

> **Nguyên tắc chung:** Cả 4 người phải kể lại được mạch *Pain → Impact → Giải pháp → Đánh giá → Chi phí*. Mỗi người tự phỏng vấn **≥1 bạn ngoài nhóm** và họp khớp bài **15 phút trước mỗi checkpoint**.

---

## 2. Việc cần làm NGAY: Chặng CP2 *(hạn 19:30 Thứ Sáu 27/11 · 4 điểm)*

**Mục tiêu bắt buộc lúc 19:30:**
- [x] `canvas.md` cập nhật số bằng chứng đầu + dòng *"Đã đổi gì so với CP1"*.
- [x] Có bằng chứng đầu (4 file phỏng vấn + số đào từ `data/preclass/`).
- [x] `spec.md §4` có sơ đồ kiến trúc giải pháp.
- [x] `eval/benchmark.csv` có **≥10 câu thử**, `eval/metric_spec.yaml` có **≥3 metric**, `data/DATA_CARD.md` bản đầu.
- [x] **Chốt cứng chuẩn "đạt" ở `spec.md §7`** *(tuyệt đối không sửa sau 19:30!)*.
- [x] `python run.py` đi hết luồng ở chế độ AI giả.

### Chia mốc thời gian (17:15 – 19:30)

1. **17:15 – 17:40 · Gom bằng chứng nhanh (cả 4 người)**
   - **An (`P1.md`), Minh (`P2.md`), Hiệp (`P3.md`), Quang (`P4.md`):** Mỗi người hỏi **1 học viên ngoài nhóm** trong lớp (10 phút/người, dùng bộ 5 câu ở Mục 6 bên dưới), chép đúng mẫu `evidence/interviews/TEMPLATE.md`, lấy **≥5 trích dẫn nguyên văn** (bỏ tên thật).
   - **An:** Chạy script đào `data/preclass/` ở máy cá nhân *(không push data gốc của BTC)* để lấy số liệu `answers.csv`, `chat.csv`, `events.csv` → ghi cách đếm vào `evidence/data-mining.md`.

2. **17:40 – 17:55 · Cả nhóm chốt thiết kế chung (15 phút)**
   - Chốt luồng hoạt động của trợ lý: nhận *(ngữ cảnh đoạn bài + tín hiệu hành vi)* → quyết định **không xen vào** hay **can thiệp 1 kiểu gỡ kẹt** *(ẩn dụ đời thường / sơ đồ Mermaid ngắn / 1 câu hỏi gợi mở, bắt buộc kèm mã đoạn bài)*.
   - Chốt chỗ chặn rủi ro: **0% lộ đáp án quiz**, **0% bịa ngoài đoạn bài**, phân biệt *rời tab đi việc riêng* vs *đang đọc kẹt*.

3. **17:55 – 19:10 · Chia 2 cặp chạy song song (75 phút)**
   - **Cặp 1 (An + Quang) — Spec, Data & Khung code:**
     - **Quang:** Vẽ sơ đồ kiến trúc Mermaid vào `spec.md §4`; tạo bộ ~10–15 đoạn bài học AI20K đánh mã đoạn (vd `D06-S01`, `D13-S02`) trong `data/`; viết `data/DATA_CARD.md` bản đầu; viết khung `codebase/tools.py` + `codebase/agent.py` chạy được `python run.py` chế độ giả.
     - **An:** Cập nhật `canvas.md` (dòng 4 + dòng *CP2*); hoàn thiện `evidence/data-mining.md`; điền bảng Impact nháp `spec.md §2` (≥3 hướng, giữ lại hướng bị loại).
   - **Cặp 2 (Hiệp + Minh) — Chỗ khó, Metric & Bộ câu thử CP2:**
     - **Hiệp:** Viết 4 lớp chỗ khó + ≥6 kịch bản + 2 kịch bản tấn công vào `spec.md §5–§6`; điền `eval/metric_spec.yaml` (≥3 metric đo được, có điều kiện cứng); viết **≥10 câu thử** vào `eval/benchmark.csv` (≥1/3 `nguoi_dung:`/`data_that:`, đủ `thuong`, `kho`, `tu_choi`).
     - **Minh:** Chấm thử độc lập 5 mẫu cùng Hiệp theo `metric_spec.yaml` (khớp ≥4/5 mới chốt); chốt chuẩn "đạt" vào `spec.md §7`; nháp `cost/personas.yaml` (3 kiểu học viên: học đều · ôn dồn · hay kẹt).

4. **19:10 – 19:30 · Tự soát & Nộp CP2 (20 phút)**
   - Chạy `python run.py check` và `python run.py`.
   - **Quang** thử nối 1 API key vào `.env` cục bộ trước khi rời lớp, chạy `python run.py eval --try` thấy `tokens > 0` để tối không bị kẹt.
   - Push Git → **An** nộp form CP2 trước **19:30**.

---

## 3. Chặng CP3 *(19:30 Thứ Sáu → 10:00 Thứ Bảy 28/11 · 4 điểm)*

**Mục tiêu bắt buộc lúc 10:00 Thứ Bảy:**
- [x] Bằng chứng đủ ngưỡng ≥1 nguồn + ≥5 trích dẫn (`evidence/summary.md`) + bảng Impact (`spec.md §2`).
- [x] `eval/benchmark.csv` mở rộng lên **20–30 câu** (≥5 `kho`, ≥2 `tu_choi` tấn công — chỉ thêm mới, không sửa đáp án câu cũ).
- [x] Bản chạy thử gọi **AI thật** (`codebase/ai.py` + `.env` cục bộ).
- [x] Đã chạy **Lượt 1** (`python run.py eval` → `eval/run-1.csv`) + chấm cột `pass` → chạy `python run.py score eval/run-1.csv`.
- [x] `spec.md §0–§7` đầy đủ.
- [x] **Video 30 giây** thao tác thật, AI trả lời thật (YouTube Unlisted / Drive Public, mở được tab ẩn danh).
- [x] Chạy thử `python run.py simulate --try` (10 phiên).

### Phân việc
- **Tối Thứ Sáu (20:30 – 23:00):**
  - **Quang:** Nối model thật trong `codebase/ai.py`, hoàn thiện prompt + guardrail trong `agent.py` & `tools.py`, test `python run.py eval --try`.
  - **Hiệp:** Mở rộng `eval/benchmark.csv` lên 20–30 câu, điền mục 1–4 của `eval/README.md`.
  - **An:** Chốt `evidence/summary.md` + bảng Impact có nguồn ở `spec.md §2`.
  - **Minh:** Hoàn thiện `cost/personas.yaml` (kèm giá model thật có link + ngày xem), chạy `python run.py simulate --try` khi Quang push xong.
- **Sáng Thứ Bảy (08:30 – 10:00):**
  - **08:30 – 09:15:** Cả nhóm chạy **Lượt 1** (`python run.py eval`), **Hiệp + Minh** chấm `pass` và chạy `score`.
  - **09:15 – 09:40:** **Minh** quay video 30 giây + kiểm tra link ở tab ẩn danh.
  - **09:40 – 10:00:** Soát checklist CP3, push Git, **An** nộp CP3 trước **10:00**.

---

## 4. Chặng CP4 *(10:00 – 14:30 Thứ Bảy 28/11 · 4 điểm + 4 điều kiện cứng xét giải)*

**4 điều kiện cứng bắt buộc có lúc 14:30 để xét giải:**
1. Bản chạy thử gọi AI thật ở quyết định trung tâm.
2. Bằng chứng pain ≥1 nguồn đạt ngưỡng (`evidence/`).
3. Bộ câu thử ≥20 câu + `eval/run-N.csv` đã chấm + `eval/report.md`.
4. **`demo-slides.pdf`** đặt ngay thư mục gốc repo.

### Phân việc
- **10:00 – 10:30 · Cả nhóm đọc lỗi Lượt 1:** Đọc hết câu trượt ở `eval/run-1.csv`, gom thành nhóm lỗi có tên, chốt **1 nhóm lỗi đau nhất** để cải tiến (ghi vào `spec.md §10` changelog).
- **10:30 – 13:00 · Chia 2 cặp:**
  - **Cặp A (Quang + Hiệp) — Cải tiến & Lượt 2:**
    - **Quang:** Sửa prompt/tool/guardrail theo đúng nhóm lỗi đã chốt → chạy trọn bộ `python run.py eval` ra `eval/run-2.csv`.
    - **Hiệp:** Chấm `eval/run-2.csv` → `score` → viết `eval/report.md` (≥3 lỗi chi tiết input/output/lý do, so sánh Lượt 1 → Lượt 2 với chuẩn đạt) + chốt `eval/README.md`.
  - **Cặp B (Minh + An) — Chi phí & Người dùng thử (+5đ bonus):**
    - **Minh:** Chạy `python run.py simulate --rate-from eval/run-2.csv` (≥50 phiên) → tính chi phí/task thành công, phóng lên quy mô thật (700 HV L3 / 1.000 HV cả khoá) với **3 kịch bản × ≥2 model** vào `cost/cost-estimate.md` + `spec.md §8–§9`.
    - **An + Minh:** Mời **2–3 bạn nhóm khác** dùng thử theo 5 nhịp (giao mục tiêu, không chỉ nút, ghi quan sát + trích nguyên văn) → điền `validation/log.md` + ghi rút ra vào `spec.md §10`.
- **13:00 – 14:15 · Slide & Tập Demo:**
  - **An + Minh:** Dựng slide 8 trang đúng khung guide 5.1 (mỗi trang ≥1 số liệu/trích dẫn có nguồn), xuất **`demo-slides.pdf`** ở thư mục gốc; **Minh** quay video dự phòng (1 ca thường + 1 ca khó).
  - **Cả 4 người:** Tập demo 2 phút, chia mỗi người nói ≥1 phần, tập trả lời 4 câu giám khảo hay hỏi (*vì sao chọn hình dạng này · lỗi nguy hiểm nhất · chi phí/task thành công tính thế nào · phần bạn làm là gì*).
- **14:15 – 14:30:** Soát 4 điều kiện cứng, push Git, **An** nộp CP4 trước **14:30**.

---

## 5. Chặng Demo & Hạn chót *(14:30 – 23:59 Thứ Bảy 28/11)*

- **14:30 – 18:00:** Demo Zone (14:30–16:00) & Demo Phòng (16:00–18:00). Sẵn sàng chạy câu thử lạ giám khảo đưa tại chỗ.
- **18:00 – 23:59:**
  - Sửa điểm nhỏ theo góp ý (nếu có) và ghi rõ giờ/đổi gì/vì sao vào `spec.md §10`.
  - **Cả 4 người** viết reflection cá nhân theo mẫu `reflection/TEMPLATE.md`:
    - `reflection/nguyen-nhu-duy-an.md`
    - `reflection/nguyen-minh-quang.md`
    - `reflection/dao-van-hiep.md`
    - `reflection/la-thai-minh.md`
  - Push commit cuối trước **23:59 Thứ Bảy 28/11**.

---

## 6. Bộ 5 câu hỏi phỏng vấn nhanh *(dùng ngay lúc 17:15 — 10 phút/người)*

> **Quy tắc Mom Test:** Hỏi chuyện thật đã xảy ra trong 2 tuần qua. **KHÔNG** giới thiệu ý tưởng của nhóm, **KHÔNG** hỏi *"bạn có thích tính năng X không?"*.

1. *"Trong 2 tuần qua, lần gần nhất bạn học bài pre-class mà bị khựng lại hoặc thấy khó hiểu nhất là bài nào, vào lúc mấy giờ?"*
2. *"Ngay lúc bị kẹt đoạn đó, bạn đã làm gì (tua lại, hỏi chatbot dưới bài, mở ChatGPT/Google, hay bỏ qua)? Mất khoảng bao lâu?"*
3. *"Khi làm vậy, chỗ nào làm bạn thấy bất tiện hoặc khó chịu nhất?"*
4. *"Lúc hỏi AI dưới video hoặc tra ngoài, có lần nào đọc xong vẫn chưa hiểu hoặc bị mất mạch đang học không? Kể cụ thể lần đó giúp mình."*
5. *"Nếu đoạn đó hiện gợi ý ngay bên cạnh, kiểu giải thích nào giúp bạn hiểu nhanh nhất (ví dụ đời thường, sơ đồ ngắn, hay câu hỏi gợi mở) — và khi nào bạn sẽ thấy nó làm phiền?"*

---

## 7. Quy tắc Git & Luật cấm *(đọc kỹ để không bị trừ điểm)*

- **Trước khi làm:** `git pull`
- **Khi đẩy code:** chỉ add file thuộc phần mình → kiểm `git status` → `git commit -m "..."` → `git push`
- **TUYỆT ĐỐI KHÔNG:**
  1. Commit `.env`, API key, nguyên file data BTC (`data/preclass/`), hoặc dữ liệu cá nhân thật (**−10 điểm**).
  2. Sửa **chuẩn "đạt"** (`spec.md §7`, `eval/metric_spec.yaml`) sau **19:30 Thứ Sáu 27/11** (**0 điểm** khối liên quan).
  3. Xoá câu thử trượt, sửa `expected` cho khớp output, hoặc sửa file `eval/run-*.csv` / `cost/simulate-*.csv` đã chạy (trừ điền cột `pass`, `ghi_chu`).
  4. Kẹt kỹ thuật quá **20 phút** → hỏi ngay Lab Coach của zone.
