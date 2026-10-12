# Đánh giá LLM Judge Phase B

Nhóm: chưa khai báo trong repository.

Người phụ trách: Thành viên 2 — Phase B.

Nguồn: `artifacts/judge_results.json`; run timestamp:
`2026-10-12T10:39:11.225438+00:00`.
Model generation: `gpt-4o-mini`; model judge: `gpt-4o-mini`.

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ `artifacts/answers_50q.json:answer`; B từ
`fixtures/human_labels_10q.json:model_answer`; reference từ
`fixtures/test_set_50q.json:ground_truth`.

| ID | Winner pass 1 | Winner pass 2 (quy về A/B gốc) | Final | Consistent | Scores pass 1 (A/B) | Scores pass 2 (A/B) |
|---:|---|---|---|---|---|---|
| 1 | B | B | B | Có | 0.8 / 1.0 | 0.8 / 1.0 |
| 5 | A | A | A | Có | 1.0 / 0.0 | 1.0 / 0.0 |
| 12 | A | A | A | Có | 1.0 / 0.7 | 1.0 / 0.8 |
| 21 | B | B | B | Có | 0.8 / 1.0 | 0.8 / 1.0 |
| 41 | A | A | A | Có | 1.0 / 0.0 | 1.0 / 0.0 |

Position bias count/rate: `0 / 5 = 0.0`.
Verbosity win rate: `0.6`; có 5 case decisive. Trong đó A thắng khi dài
hơn B ở 2 case và B thắng khi dài hơn A ở 1 case. Ba case còn lại winner
không dài hơn đối thủ.

Không có case không nhất quán sau khi hoán đổi vị trí. Điều này cho thấy
judge ổn định trong năm cặp đã đo, nhưng không đủ để khẳng định không tồn tại
position bias trên các dữ liệu khác. Tỷ lệ 0.6 ở đây là tỷ lệ winner dài hơn
trong các case decisive, chỉ là dấu hiệu cần theo dõi chứ không chứng minh
judge ưu tiên độ dài. Ví dụ ở cặp 21, B thắng vì súc tích hơn dù A dài hơn;
do đó độ dài không phải tiêu chí duy nhất quyết định winner.

## Calibration đúng model_answer

Helper đánh giá đúng question/model_answer đang có trong
`fixtures/human_labels_10q.json`; không lấy answer mới của pipeline. Prompt
chỉ nhận question, answer và reference. Không gửi `human_label`, `human_note`
hoặc phân bố nhãn human vào prompt.

| ID | Model answer gốc | Judge | Human | Agree |
|---:|---|---:|---:|---|
| 1 | 3 ngày làm việc có lương khi kết hôn. | 1 | 1 | Có |
| 5 | Giám đốc phòng ban phê duyệt. | 0 | 0 | Có |
| 12 | Thưởng Tết tối thiểu 1 tháng lương. | 1 | 1 | Có |
| 21 | 18 ngày phép; lương Senior 20–35 triệu. | 1 | 1 | Có |
| 23 | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | 1 | 1 | Có |
| 29 | Trưởng phòng phê duyệt; phạt 2% tháng. | 0 | 0 | Có |
| 33 | 19 ngày phép; phụ cấp 1.500.000 VNĐ/tháng. | 1 | 1 | Có |
| 41 | 12 ngày phép năm. | 0 | 0 | Có |
| 46 | Thử việc không được nghỉ phép năm. | 1 | 1 | Có |
| 50 | Được dùng NordVPN nếu kết nối an toàn. | 0 | 0 | Có |

Cohen’s κ: `1.0`.

Observed agreement là `10/10 = 1.0`. Phân bố nhãn judge và human đều có
6 nhãn 1 và 4 nhãn 0, nên chance agreement:
`(6/10 × 6/10) + (4/10 × 4/10) = 0.52`.
Vì vậy `κ = (1.0 - 0.52) / (1 - 0.52) = 1.0`, tương ứng agreement hoàn
hảo trên mẫu 10 câu này.

## Giới hạn và cách dùng judge

Phase B dùng model `gpt-4o-mini`, JSON output với winner A/B/tie, reasoning
và scores 0–1. Pairwise dùng 5 cặp, mỗi cặp chạy hai lượt đổi vị trí;
calibration dùng 10 `model_answer` gốc. Kết quả κ đạt 1.0 trên mẫu nhỏ,
nhưng không nên suy rộng thành độ tin cậy tuyệt đối của judge. Cần tiếp tục
kiểm tra trên nhiều câu hơn, đọc các reasoning lệch với human nếu xuất hiện,
và duy trì swap-and-average để phát hiện position bias. Judge chỉ là công cụ
đánh giá có kiểm soát, không thay thế human review hoặc reference policy.
