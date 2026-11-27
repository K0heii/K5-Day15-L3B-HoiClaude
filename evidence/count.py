"""Script đếm bằng chứng hành vi từ bộ data thật BTC cấp (`data/preclass/`).

Cách chạy:
    python evidence/count.py <duong-dan-toi-thu-muc-data-preclass>

Chỉ dùng thư viện chuẩn của Python. Không lưu hay xuất dữ liệu cá nhân;
mọi mã học viên / mã dòng đều giữ nguyên dạng đã ẩn danh của BTC (`L0001`, `A00001`, `C00001`...).
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta


def load_csv(folder, filename):
    path = os.path.join(folder, filename)
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pct(x, n):
    return (x / n * 100.0) if n else 0.0


def parse_utc(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python evidence/count.py <duong-dan-toi-thu-muc-data-preclass>")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        sys.exit(f"Không tìm thấy thư mục: {folder}")

    learners = load_csv(folder, "learners.csv")
    answers = load_csv(folder, "answers.csv")
    chat = load_csv(folder, "chat.csv")
    completed = load_csv(folder, "completed_items.csv")
    rewards = load_csv(folder, "rewards.csv")

    # --- 1. Phân tích events.csv (107.709 dòng) ---
    events_path = os.path.join(folder, "events.csv")
    total_events = 0
    active_hv = set()
    min_dt, max_dt = None, None
    vn_hours = Counter()
    hv_days = defaultdict(set)
    hv_sessions = Counter()
    hv_video_events = Counter()

    vo_pairs, ve_pairs = set(), set()
    vo_total, ve_total = 0, 0

    seek_total = seek_back = seek_fwd = seek_crossed = 0
    seek_back_hv = set()
    seek_back_by_hv = Counter()
    seek_examples = []

    flush_total = flush_pause_ge1 = flush_pause_ge3 = flush_hidden_ge1 = 0
    flush_stuck_hv = set()
    flush_stuck_by_hv = Counter()
    flush_examples = []

    vis_false = vis_true = 0
    vis_false_hv = set()

    quiz_opened = quiz_dismissed = quiz_skipped = 0
    quiz_skipped_hv = set()
    quiz_skip_examples = []

    ai_shown = 0
    ai_shown_hv = set()

    ar_total = ar_missing_ctx = ar_no_citation = 0
    ar_verdicts = Counter()
    ar_reply_kinds = Counter()
    ar_no_cite_examples = []

    lab_opened = lab_completed = lab_skipped = 0

    with open(events_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            total_events += 1
            t = row["type"]
            hv = row["hv"]
            if hv:
                active_hv.add(hv)

            dt = parse_utc(row["occurred_at"])
            if dt is not None:
                if min_dt is None or dt < min_dt:
                    min_dt = dt
                if max_dt is None or dt > max_dt:
                    max_dt = dt
                vn_dt = dt + timedelta(hours=7)
                if t in ("session_started", "video_opened", "lecture_opened"):
                    vn_hours[vn_dt.hour] += 1
                if hv:
                    hv_days[hv].add(vn_dt.date().isoformat())

            if t == "session_started" and hv:
                hv_sessions[hv] += 1

            raw = row["data"]
            jd = {}
            if raw and raw.startswith("{"):
                try:
                    jd = json.loads(raw)
                except json.JSONDecodeError:
                    jd = {}

            if t == "video_opened":
                vo_total += 1
                if hv and row["video"]:
                    vo_pairs.add((hv, row["video"]))
                    hv_video_events[hv] += 1
            elif t == "video_ended":
                ve_total += 1
                if hv and row["video"]:
                    ve_pairs.add((hv, row["video"]))
            elif t == "video_seeked":
                seek_total += 1
                fr, to = jd.get("from"), jd.get("to")
                if isinstance(fr, (int, float)) and isinstance(to, (int, float)):
                    if to < fr:
                        seek_back += 1
                        if hv:
                            seek_back_hv.add(hv)
                            seek_back_by_hv[hv] += 1
                        if len(seek_examples) < 5 and row["lesson_id"] and (fr - to) >= 20:
                            seek_examples.append(
                                (row_num, hv, row["lesson_id"], row["video"], round(fr, 1), round(to, 1), row["occurred_at"])
                            )
                    elif to > fr:
                        seek_fwd += 1
                if jd.get("crossed_stop") is True:
                    seek_crossed += 1
            elif t == "video_segments_flushed":
                flush_total += 1
                pauses = jd.get("pauses") or 0
                hidden = jd.get("hidden_count") or 0
                if pauses >= 1:
                    flush_pause_ge1 += 1
                if pauses >= 3:
                    flush_pause_ge3 += 1
                    if hv:
                        flush_stuck_hv.add(hv)
                        flush_stuck_by_hv[hv] += 1
                    if len(flush_examples) < 5 and hidden >= 1 and (row["video"] or row["lesson_id"]):
                        flush_examples.append(
                            (row_num, hv, row["lesson_id"] or "-", row["video"] or "-", pauses, hidden, jd.get("duration"), row["occurred_at"])
                        )
                if hidden >= 1:
                    flush_hidden_ge1 += 1
            elif t == "app_visibility_changed":
                if jd.get("visible") is False:
                    vis_false += 1
                    if hv:
                        vis_false_hv.add(hv)
                elif jd.get("visible") is True:
                    vis_true += 1
            elif t == "quiz_item_opened":
                quiz_opened += 1
            elif t == "quiz_item_dismissed":
                quiz_dismissed += 1
                if jd.get("skipped_stop") is True:
                    quiz_skipped += 1
                    if hv:
                        quiz_skipped_hv.add(hv)
                    if len(quiz_skip_examples) < 5 and row["lesson_id"]:
                        quiz_skip_examples.append(
                            (row_num, hv, row["lesson_id"], row["video"], jd.get("question_id"), row["occurred_at"])
                        )
            elif t == "agent_message_shown":
                ai_shown += 1
                if hv:
                    ai_shown_hv.add(hv)
            elif t == "agent_replied":
                ar_total += 1
                if jd.get("missing_context") is True:
                    ar_missing_ctx += 1
                if not jd.get("moc_trich_dan"):
                    ar_no_citation += 1
                    if len(ar_no_cite_examples) < 3 and row["ref_id"]:
                        ar_no_cite_examples.append((row_num, hv, row["ref_id"], jd.get("missing_context"), row["occurred_at"]))
                ar_verdicts[str(jd.get("verdict"))] += 1
                ar_reply_kinds[str(jd.get("reply_kind"))] += 1
            elif t == "lab_opened":
                lab_opened += 1
            elif t == "lab_completed":
                lab_completed += 1
                if jd.get("skipped") is True:
                    lab_skipped += 1

    # --- 2. Phân tích answers.csv ---
    first_scored = [r for r in answers if r["lan_thu"] == "1" and r["was_correct"] in ("True", "False")]
    first_wrong = [r for r in first_scored if r["was_correct"] == "False"]
    first_wrong_hv = {r["hv"] for r in first_wrong if r["hv"]}
    first_scored_hv = {r["hv"] for r in first_scored if r["hv"]}

    wrong_by_lesson = defaultdict(lambda: [0, 0])
    for r in first_scored:
        wrong_by_lesson[r["lesson_id"]][0] += 1
        if r["was_correct"] == "False":
            wrong_by_lesson[r["lesson_id"]][1] += 1

    wrong_examples = [
        (r["id"], r["hv"], r["lesson_id"], r["nguon"], r["kc_code"], r["created_at"])
        for r in first_wrong
        if r["lesson_id"] in ("program-day13:launch-economics", "program-day06:data-engineering-for-agents")
    ][:5]

    # --- 3. Phân tích chat.csv + rubric trong answers.csv ---
    chat_ans_by_ref = {r["ref"]: r for r in answers if r["nguon"] == "chat"}
    scored_chats = [c for c in chat if chat_ans_by_ref.get(c["id"], {}).get("rubric_bam_bai") in ("0", "1", "2")]
    offtopic_chats = [c for c in scored_chats if chat_ans_by_ref[c["id"]]["rubric_bam_bai"] == "0"]
    passive_chats = [c for c in scored_chats if chat_ans_by_ref[c["id"]]["rubric_y_moi"] == "0"]
    short_chats = [c for c in chat if c["do_dai_cau_hoi"].isdigit() and int(c["do_dai_cau_hoi"]) <= 20]
    short_offtopic = [c for c in short_chats if chat_ans_by_ref.get(c["id"], {}).get("rubric_bam_bai") == "0"]
    true_replies = [r for r in answers if r["nguon"] == "chat" and r["la_reply_that"] == "True"]
    reply_kind_chat = [c for c in chat if c["kind"] == "reply"]

    def avg_reply_len(rows):
        vals = [int(r["do_dai_tra_loi"]) for r in rows if r["do_dai_tra_loi"].isdigit()]
        return sum(vals) / len(vals) if vals else 0.0

    chat_examples = [
        (
            c["id"],
            c["hv"],
            c["transcript"],
            c["do_dai_cau_hoi"],
            c["do_dai_tra_loi"],
            chat_ans_by_ref.get(c["id"], {}).get("rubric_bam_bai", ""),
            chat_ans_by_ref.get(c["id"], {}).get("rubric_y_moi", ""),
        )
        for c in short_offtopic
        if c["transcript"]
    ][:5]

    # --- 4. Thời điểm học (giờ Việt Nam UTC+7) & Phân bố tần suất học viên ---
    tot_h = sum(vn_hours.values())
    eve_18_24 = sum(vn_hours[h] for h in range(18, 24))
    eve_18_02 = sum(vn_hours[h] for h in [18, 19, 20, 21, 22, 23, 0, 1])

    day_counts = sorted(len(v) for v in hv_days.values())
    n_active = len(active_hv)
    low_freq = sum(1 for x in day_counts if x <= 2)
    mid_freq = sum(1 for x in day_counts if 3 <= x <= 6)
    high_freq = sum(1 for x in day_counts if x >= 7)

    # Tín hiệu kẹt gộp theo học viên (có ít nhất 1 trong: tua ngược >=2 lần, dừng >=3 lần/quãng, hoặc làm sai lần đầu)
    hv_rewind_2plus = {hv for hv, cnt in seek_back_by_hv.items() if cnt >= 2}
    hv_any_friction = hv_rewind_2plus | flush_stuck_hv | first_wrong_hv

    # Tổng lượt sự kiện kẹt trên tập học viên bị kẹt (để ước lượng tần suất/tháng)
    wrong_by_hv = Counter(r["hv"] for r in first_wrong if r["hv"])
    friction_events_per_hv = [
        seek_back_by_hv[hv] + flush_stuck_by_hv[hv] + wrong_by_hv[hv]
        for hv in hv_any_friction
    ]
    friction_events_per_hv.sort()
    avg_friction_21d = sum(friction_events_per_hv) / len(friction_events_per_hv) if friction_events_per_hv else 0.0
    med_friction_21d = friction_events_per_hv[len(friction_events_per_hv) // 2] if friction_events_per_hv else 0

    # --- IN KẾT QUẢ ---
    print("=== TỔNG QUAN TẬP DỮ LIỆU ===")
    print(f"Khoảng thời gian (UTC): {min_dt} -> {max_dt}")
    print(f"Tổng tài khoản (learners.csv): {len(learners)} | Học viên có hoạt động (events.csv): {n_active} ({pct(n_active, len(learners)):.1f}%)")
    print(f"Tổng dòng: events={total_events} | answers={len(answers)} | chat={len(chat)} | completed_items={len(completed)} | rewards={len(rewards)}")
    print()

    print("=== 1. HÀNH VI TUA / DỪNG / CHUYỂN TAB / BỎ DỞ VIDEO (events.csv) ===")
    ended_in_opened = len(vo_pairs & ve_pairs)
    not_ended = len(vo_pairs) - ended_in_opened
    print(f"Cặp (học viên, video) mở nhưng KHÔNG xem tới cuối: {not_ended}/{len(vo_pairs)} ({pct(not_ended, len(vo_pairs)):.1f}%) [mở: {len(vo_pairs)}, xem hết: {ended_in_opened}]")
    print(f"Lượt tua ngược video (to < from): {seek_back}/{seek_total} ({pct(seek_back, seek_total):.1f}%) — gặp ở {len(seek_back_hv)}/{n_active} HV hoạt động ({pct(len(seek_back_hv), n_active):.1f}%)")
    print(f"Lượt tua bỏ qua câu hỏi giữa video (crossed_stop=True): {seek_crossed}/{seek_total} ({pct(seek_crossed, seek_total):.1f}%)")
    print(f"Quãng xem video có dừng >=1 lần (pauses>=1): {flush_pause_ge1}/{flush_total} ({pct(flush_pause_ge1, flush_total):.1f}%)")
    print(f"Quãng xem video dừng liên tục >=3 lần (pauses>=3): {flush_pause_ge3}/{flush_total} ({pct(flush_pause_ge3, flush_total):.1f}%) — gặp ở {len(flush_stuck_hv)}/{n_active} HV ({pct(len(flush_stuck_hv), n_active):.1f}%)")
    print(f"Quãng xem video có chuyển tab/ẩn app (hidden_count>=1): {flush_hidden_ge1}/{flush_total} ({pct(flush_hidden_ge1, flush_total):.1f}%)")
    print(f"Tổng lượt rời tab (app_visibility_changed visible=False): {vis_false} lượt trên {len(vis_false_hv)}/{n_active} HV ({pct(len(vis_false_hv), n_active):.1f}%)")
    print(f"Câu hỏi giữa video bị đóng bỏ qua (skipped_stop=True): {quiz_skipped}/{quiz_dismissed} lượt đóng ({pct(quiz_skipped, quiz_dismissed):.1f}%), trên {len(quiz_skipped_hv)}/{n_active} HV ({pct(len(quiz_skipped_hv), n_active):.1f}%)")
    print(f"Học viên có >=1 dấu hiệu kẹt rõ (tua ngược >=2 lần HOẶC dừng >=3 lần/quãng HOẶC làm sai lần đầu): {len(hv_any_friction)}/{n_active} ({pct(len(hv_any_friction), n_active):.1f}%)")
    print(f"  -> Tần suất tín hiệu kẹt trên nhóm {len(hv_any_friction)} HV trong 21 ngày: trung vị={med_friction_21d} lần, TB={avg_friction_21d:.1f} lần (~{med_friction_21d * 30 / 21:.1f} đến {avg_friction_21d * 30 / 21:.1f} lần/tháng)")
    print()

    print("=== 2. LÀM SAI LẦN ĐẦU (answers.csv, lan_thu=1) ===")
    print(f"Tổng lần thử đầu làm sai: {len(first_wrong)}/{len(first_scored)} ({pct(len(first_wrong), len(first_scored)):.1f}%) — {len(first_wrong_hv)}/{len(first_scored_hv)} HV có làm bài ({pct(len(first_wrong_hv), len(first_scored_hv)):.1f}%)")
    print("Top 5 bài có tỉ lệ sai lần đầu cao nhất (n >= 20 câu):")
    top_wrong = sorted(
        [(w / n, w, n, lid) for lid, (n, w) in wrong_by_lesson.items() if n >= 20],
        reverse=True,
    )
    for rate, w, n, lid in top_wrong[:5]:
        print(f"  - {lid}: {w}/{n} ({rate * 100:.1f}%)")
    sua_sai = sum(1 for r in rewards if r["hanh_vi"] == "sua_sai")
    print(f"Số lần được thưởng sua_sai (rewards.csv): {sua_sai} / {len(first_wrong)} câu làm sai lần đầu ({pct(sua_sai, len(first_wrong)):.1f}%)")
    print()

    print("=== 3. HỎI AI THỤ ĐỘNG & AI CHỦ ĐỘNG XEN VÀO THIẾU LỌC (chat.csv + events.csv) ===")
    print(f"Lượt hỏi AI được chấm rubric không tạo ý mới (rubric_y_moi=0): {len(passive_chats)}/{len(scored_chats)} ({pct(len(passive_chats), len(scored_chats)):.1f}%)")
    print(f"Lượt hỏi AI lạc đề / không bám bài (rubric_bam_bai=0): {len(offtopic_chats)}/{len(scored_chats)} ({pct(len(offtopic_chats), len(scored_chats)):.1f}%) — AI vẫn trả lời TB {avg_reply_len(offtopic_chats):.0f} ký tự")
    print(f"Câu hỏi quá ngắn <=20 ký tự: {len(short_chats)}/{len(chat)} ({pct(len(short_chats), len(chat)):.1f}%) — trong đó lạc đề {len(short_offtopic)}/{len(short_chats)} ({pct(len(short_offtopic), len(short_chats)):.1f}%), AI vẫn trả lời TB {avg_reply_len(short_chats):.0f} ký tự")
    print(f"Lời AI bạn học tự xen vào (agent_message_shown): {ai_shown} lần (trên {len(ai_shown_hv)} HV) vs lượt học viên thực sự trả lời lại AI (la_reply_that=True): {len(true_replies)}/{ai_shown} ({pct(len(true_replies), ai_shown):.2f}%) [chat kind=reply: {len(reply_kind_chat)}]")
    print(f"Phản hồi AI (agent_replied): {ar_total} | không có mốc trích dẫn (moc_trich_dan rỗng): {ar_no_citation}/{ar_total} ({pct(ar_no_citation, ar_total):.1f}%) | missing_context=True: {ar_missing_ctx}/{ar_total} ({pct(ar_missing_ctx, ar_total):.1f}%)")
    print()

    print("=== 4. KHUNG GIỜ HỌC (GIỜ VN UTC+7) & PHÂN BỐ PERSONA (05/11 -> 25/11) ===")
    print(f"Sự kiện mở phiên/bài/video (N={tot_h}): 18h-24h VN = {eve_18_24}/{tot_h} ({pct(eve_18_24, tot_h):.1f}%), 18h-02h VN = {eve_18_02}/{tot_h} ({pct(eve_18_02, tot_h):.1f}%)")
    print(f"Phân bố số ngày học có hoạt động / HV (N={n_active} trong 21 ngày):")
    print(f"  - Dùng ít (1-2 ngày): {low_freq}/{n_active} ({pct(low_freq, n_active):.1f}%)")
    print(f"  - Dùng vừa (3-6 ngày): {mid_freq}/{n_active} ({pct(mid_freq, n_active):.1f}%)")
    print(f"  - Dùng nhiều (>=7 ngày): {high_freq}/{n_active} ({pct(high_freq, n_active):.1f}%)")
    print()

    print("=== 5. VÍ DỤ CỤ THỂ (ẨN DANH, TRÍCH TRỰC TIẾP TỪ DATA) ===")
    print("Video seek ngược >=20s:", seek_examples[:3])
    print("Video dừng >=3 lần + chuyển tab >=1 lần:", flush_examples[:3])
    print("Bỏ qua câu hỏi giữa video (skipped_stop=True):", quiz_skip_examples[:3])
    print("Làm sai lần đầu ở bài nặng (Day 06 / Day 13):", wrong_examples[:3])
    print("Hỏi ngắn <=20 ký tự, bam_bai=0 nhưng AI trả lời dài:", chat_examples[:3])
    print("AI trả lời không có mốc trích dẫn:", ar_no_cite_examples[:3])


if __name__ == "__main__":
    main()
