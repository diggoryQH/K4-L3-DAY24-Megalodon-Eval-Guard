# Nhóm thực hiện K4 Track 3B

Tên nhóm: Group 1 - K4 Track 3B

Repo chung: https://github.com/diggoryQH/K4-L3-DAY24-Megalodon-Eval-Guard

Trưởng nhóm/người nộp: Ngụy Quang Hùng - 2A202602998

Ngày lab/deadline áp dụng: 23:59 13/10/2026 — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: 55edca2a016060a5392b15b1d1c6f49e6fc8635d

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.
Thêm/xóa rows để khớp nhóm thật; mẫu ba rows không ép nhóm phải có ba người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Ngụy Quang Hùng | 2A202602998 | Người 1: Phase A RAGAS evaluation, m4_eval adapter, setup answers | src/phase_a_ragas.py, failure_clusters.md, answers_50q.json, ragas_50q.json |
| 2 | Đinh Văn Bình | 2A202602999 | Người 2: Phase B LLM Judge, Pairwise, Calibration, Bias | src/phase_b_judge.py, bias_report.md, judge_results.json |
| 3 | Nguyễn Văn Việt | 2A202603000 | Người 3: Phase C Guardrails (Presidio + NeMo), Blueprint CI/CD, Tích hợp | src/phase_c_guard.py, blueprint.md, guard_results.json |

Người tích hợp/chạy batch/nộp link: Nguyễn Văn Việt và Ngụy Quang Hùng cùng tích hợp các phase, chạy check_lab.py và push lên repository.

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: Windows 11, Python 3.12.8, GCC/MSVC.
Virtualenv/dependencies/imports: Đã cài đặt các gói cần thiết từ requirements.txt bao gồm presidio-analyzer, presidio-anonymizer, nemoguardrails, ragas, sentence-transformers, qdrant-client.
Models/Qdrant/50 answers đã chuẩn bị: Docker Qdrant chạy cổng 6333, collection lab24_production index 107 chunks, sinh đủ 50 câu trả lời bằng gpt-4o-mini lưu tại artifacts/answers_50q.json.
Nếu cài full NeMo chưa thành công, ghi lỗi thực tế; không dùng unit test pass hoặc pip resolve để khẳng định runtime đã chạy: NeMo Guardrails chạy thành công với cấu hình guardrails/config.yml và rails.co với model gpt-4o-mini.

## INDIVIDUAL

### NguyQuangHung-2A202602998

- Phần được giao và phần thực tế đã làm: Phụ trách Phase A (Tasks 1-4), xây dựng hàm group_by_distribution, run_ragas_50q, bottom_10, cluster_analysis trong phase_a_ragas.py; tích hợp adapter m4_eval; dựng Docker Qdrant và chạy setup_answers.py tạo 50 answers thật.
- Bằng chứng: File src/phase_a_ragas.py, doc/reports/failure_clusters.md, artifacts/answers_50q.json và artifacts/ragas_50q.json.
- Cách kiểm tra: Chạy pytest tests/test_phase_a.py (6/6 passed) và python scripts/run_experiments.py --phase a --live (50/50 câu đánh giá thành công).
- Điều đã học: Hiểu sâu 4 metric của RAGAS, bản chất của bẫy adversarial và nguyên nhân gây giảm faithfulness trong các câu hỏi đa bước (multi-hop).
- Giới hạn/cách xử lý: Mô hình evaluator có thể tốn thời gian khi chạy đồng bộ; xử lý bằng cách cấu hình unbuffered IO và theo dõi tiến độ log.
- Nguồn/AI hỗ trợ nếu có: Sử dụng tài liệu RAGAS, gợi ý từ code lab và tự kiểm chứng qua contract validation.

### DinhVanBinh-2A202602999

- Phần được giao và phần thực tế đã làm: Phụ trách Phase B (Tasks 5-8), hiện thực hóa pairwise_judge, swap_and_average, cohen_kappa, bias_report trong phase_b_judge.py; đánh giá position bias và verbosity bias.
- Bằng chứng: File src/phase_b_judge.py, doc/reports/bias_report.md, artifacts/judge_results.json.
- Cách kiểm tra: Chạy pytest tests/test_phase_b.py (8/8 passed) và python scripts/run_experiments.py --phase b --live.
- Điều đã học: Hiểu cách khắc phục position bias bằng kỹ thuật swap-and-average, cách đo đạc độ tin cậy gán nhãn qua hệ số Cohen's Kappa.
- Giới hạn/cách xử lý: Đảm bảo prompt đánh giá nhị phân độc lập không bị rò rỉ nhãn con người; xử lý bằng cách tuân thủ đúng hợp đồng judge_binary.
- Nguồn/AI hỗ trợ nếu có: Tham khảo tài liệu LLM-as-a-judge và tự kiểm chứng qua các bộ test mock.

### NguyenVanViet-2A202603000

- Phần được giao và phần thực tế đã làm: Phụ trách Phase C (Tasks 9-12) và tích hợp, hiện thực hóa pii_scan, check_input_rail, check_output_rail, run_adversarial_suite, measure_p95_latency trong phase_c_guard.py; viết báo cáo blueprint.md.
- Bằng chứng: File src/phase_c_guard.py, doc/reports/blueprint.md, artifacts/guard_results.json.
- Cách kiểm tra: Chạy pytest tests/test_phase_c.py (12/12 passed) và python scripts/run_experiments.py --phase c --live.
- Điều đã học: Cách xây dựng hệ thống phòng vệ đa tầng kết hợp giữa rule-based regex (Presidio) và LLM Rails (NeMo Guardrails), phân tích độ trễ P95.
- Giới hạn/cách xử lý: Presidio mặc định nhận diện nhầm thực thể tiếng Anh trên câu tiếng Việt; xử lý bằng cách lọc đúng tập thực thể PII nhạy cảm (VN_CCCD, VN_PHONE, EMAIL_ADDRESS).
- Nguồn/AI hỗ trợ nếu có: Tham khảo tài liệu Presidio và NeMo Guardrails, tự kiểm tra qua check_lab.py.

## Cập nhật sau khi nộp

Không có cập nhật bổ sung sau deadline; toàn bộ mã nguồn và báo cáo được hoàn thiện và kiểm thử đồng bộ trước thời hạn.
