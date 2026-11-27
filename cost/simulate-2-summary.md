# Tóm tắt mô phỏng simulate-2@20261128-002614

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoc_it | 23 | 1 | 387 | 65 | 0.8 | 2.6 |
| hoc_vua | 24 | 2 | 630 | 102 | 1.2 | 4.7 |
| hoc_nhieu | 3 | 2 | 664 | 128 | 1.3 | 5.0 |

Tỉ lệ đạt dùng để tính: 24/24 (100%) — lượt run-3@20261128-000606

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.5-flash-lite (vào 0.3 · ra 2.5 $/1M) | $0.00037 | $0.00037 | $0.00024 | $0.7306 | $1.70 | $2.44 | $0.0024 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0014 | $0.0014 | $0.00093 | $2.79 | $6.51 | $9.30 | $0.0093 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.5) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.5-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
