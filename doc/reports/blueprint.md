# Blueprint CI/CD cho RAG và guardrails

Nhóm: Group 1 - K4 Track 3B

Người phụ trách: Nguyễn Văn Việt - 2A202603000

Đây là **đề xuất CI/CD**, không phải workflow đã được triển khai/chạy.
Nguồn kết quả: artifacts/ragas_50q.json, judge_results.json, guard_results.json.
Run timestamp: 2026-10-12T10:56:33.068191+00:00; guard models: gpt-4o-mini.
Models generation/evaluator/judge từ A/B: Generation: gpt-4o-mini (answers_50q.json); Evaluator: gpt-4o-mini, text-embedding-ada-002 (ragas_50q.json); Judge: gpt-4o-mini (judge_results.json).

## Kiến trúc và failure action

Input → Presidio → NeMo input → RAG → NeMo output → response.
Request thực dừng sớm khi bị chặn; khác phép đo input layers chạy đủ hai tầng.

Mô tả data flow và các thành phần:
1. Input Layer: Câu hỏi người dùng gửi vào trước hết đi qua tầng Presidio PII Scanner để lọc các thực thể định danh cá nhân nhạy cảm (CCCD/CMND, số điện thoại, email). Nếu phát hiện PII (như trong trường hợp rò rỉ dữ liệu cá nhân), request lập tức bị chặn (failure action: abort và trả về thông báo lỗi vi phạm chính sách bảo mật). Nếu an toàn, query đi tiếp vào NeMo Guardrails Input Rails (kiểm tra jailbreak, off-topic, prompt injection). Nếu vi phạm, hệ thống dừng sớm và trả về lời từ chối theo kịch bản quy định (rails.co).
2. Processing & Generation Layer: Khi input hợp lệ, query được đưa vào hệ thống RAG (Hybrid Search BM25 + Qdrant Dense, sau đó Cross-Encoder Reranker chọn top-3 ngữ cảnh) và gửi tới LLM generation (gpt-4o-mini) với prompt ràng buộc chặt chẽ.
3. Output Layer: Câu trả lời sinh ra từ LLM được đưa qua NeMo Guardrails Output Rails để kiểm tra tính an toàn thông tin (chặn rò rỉ PII, bí mật kinh doanh hoặc nội dung vi phạm chính sách). Nếu phát hiện vi phạm, output rail thay thế câu trả lời bằng phản hồi an toàn định sẵn.
4. Logging, Secrets & Fallback: Toàn bộ log đều được ẩn danh (redacted) trước khi lưu trữ (không lưu PII dạng plain text). API keys và credentials được quản lý bảo mật qua biến môi trường hoặc Secret Manager, không hardcode trong mã nguồn. Trong trường hợp dịch vụ LLM gặp sự cố hoặc timeout, hệ thống kích hoạt extractive fallback trả về đoạn trích tài liệu kèm cảnh báo.

## Phạm vi và số đo latency

Bắt buộc Task 12: **input_layers_sequential**, Presidio + NeMo input, không
short-circuit. Engines tạo trước đo; có hai warm-up thật không tính vào mẫu.
Percentile nội suy tuyến tính từ raw samples; tổng từ tổng từng sample.

Số mẫu timed: 20; warm-up: 2; phương pháp: linear.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | 11.2408 | 13.7877 | 14.8838 | Đạt ngân sách riêng lẻ |
| NeMo input | 1529.2696 | 3284.9587 | 3588.8636 | Vượt ngân sách 500ms |
| Input guard sequential | 1543.1893 | 3297.1867 | 3600.7300 | Vượt ngân sách 500ms |
| RAG | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| NeMo output | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| Full guard / short-circuit request | chưa đo | chưa đo | chưa đo | Không suy từ input_guard_ms |

Input-layer budget target: 500ms; kết quả thực tế/budget_ok: P95 = 3297.1867ms, budget_ok = False.
Phân tích điểm nghẽn (bottleneck):
- Tầng Presidio hoạt động rất nhanh trên môi trường CPU (P95 đạt 13.79ms), hoàn toàn đáp ứng kỳ vọng cho tầng lọc tĩnh.
- Điểm nghẽn chính nằm ở NeMo input rail (P95 đạt 3284.96ms, chiếm hơn 99% tổng thời gian input guard). Nguyên nhân là do NeMo thực hiện gọi API LLM (gpt-4o-mini) qua mạng để đánh giá intent và self-check jailbreak, dẫn đến độ trễ mạng và thời gian suy luận phụ thuộc trực tiếp vào dịch vụ đám mây.
- Các thành phần ngoài phạm vi bắt buộc (RAG pipeline, NeMo output rail, full end-to-end guard short-circuit) được giữ nguyên trạng thái "chưa đo". Để đo đạc chính xác các thành phần này trong tương lai, kế hoạch triển khai bao gồm: lấy tối thiểu 30 mẫu có gắn timestamp độ chính xác cao (time.perf_counter), thực hiện 3 lượt warm-up độc lập cho từng module, và đo đạc trong điều kiện tải mạng ổn định.

## CI gates đề xuất

- RAGAS faithfulness ≥0.75, avg_score ≥0.65 trên 50 câu.
- Attacks ≥18/20 cho CI đề xuất; clean 8/8 allowed; output cases đúng.
- Full guard P95 <500ms chỉ áp dụng sau khi thực sự đo full guard.

Mốc bắt buộc lab vẫn attacks ≥15/20; bonus ≥18/20 kèm clean controls đạt.
Đề xuất triển khai CI Runner:
- Lệnh thực thi kiểm tra trong pipeline CI (ví dụ GitHub Actions):
  `python scripts/run_experiments.py --phase all --live`
  `python scripts/check_lab.py --with-tests`
- Script kiểm tra sẽ thoát với mã lỗi nonzero (`exit 1`) nếu bất kỳ ngưỡng nào không được thỏa mãn:
  - Nếu kết quả RAGAS có faithfulness < 0.75 hoặc avg_score < 0.65.
  - Nếu số lượng test case tấn công bị chặn < 18/20 (ngưỡng đề xuất CI) hoặc < 15/20 (ngưỡng bắt buộc của bài lab).
  - Nếu có bất kỳ false positive nào trên bộ dữ liệu sạch (clean pass rate != 100%, false_positive_rate > 0).
  - Nếu bất kỳ trường hợp output safety nào bị phân loại sai hoặc rò rỉ dữ liệu nhạy cảm.
- Quy trình này hiện tại ở mức đề xuất kiến trúc (chưa triển khai standing CI server tự động), toàn bộ kiểm thử hiện tại được thực thi thủ công qua test harness nội bộ.

## Monitoring và cải tiến

Giám sát trong môi trường production:
- Các chỉ số cần theo dõi (metrics): Tỷ lệ chặn đầu vào theo từng danh mục (PII block rate, jailbreak block rate, off-topic rate), tỷ lệ false positive do người dùng báo cáo, độ trễ P50/P95/P99 theo từng chặng, điểm đánh giá chất lượng phản hồi ngẫu nhiên từ LLM Judge định kỳ (sample 5% traffic).
- Ngưỡng cảnh báo: Cảnh báo ngay lập tức nếu P95 latency vượt quá 4000ms trong 5 phút liên tục, hoặc tỷ lệ chặn input tăng đột biến vượt 25% (nghi ngờ tấn công DoS hoặc luật guardrail quá nghiêm ngặt).
- Xử lý drift và false positive: Định kỳ thu thập các mẫu bị chặn được người dùng kháng nghị, phân tích nguyên nhân và cập nhật lại bộ luật Colang hoặc regex recognizer của Presidio. Đảm bảo dữ liệu người dùng luôn được mã hóa trong quá trình điều tra sự cố.

Số liệu thực nghiệm đạt được từ hệ thống:
- RAGAS mean score: 0.7989; worst distribution: multi_hop (0.6931).
- Cohen’s κ: 1.0 (sự đồng thuận tuyệt đối giữa LLM Judge và nhãn con người trên 10 câu chuẩn hóa).
- Attacks passed: 20/20 (100%); clean false_positive_rate: 0.0 (0/8 câu sạch bị chặn nhầm).

Các hành động cải tiến cụ thể có thể kiểm chứng:
1. Tối ưu hóa độ trễ NeMo: Thay thế việc gọi cloud LLM bằng một mô hình phân loại cục bộ nhỏ (như DeBERTa hoặc ModernBERT fine-tuned) cho tác vụ kiểm tra jailbreak và off-topic để giảm P95 latency của NeMo input từ 3284ms xuống dưới 200ms.
2. Nâng cao chất lượng Multi-hop: Bổ sung cơ chế truy vấn phân rã (query decomposition) và Chain-of-Thought prompting để nâng điểm Faithfulness của nhóm multi_hop từ 0.3856 lên trên 0.8000.
3. Mở rộng tập kiểm thử: Bổ sung thêm ít nhất 50 mẫu adversarial đa ngôn ngữ và tiếng lóng tiếng Việt để kiểm tra độ bền vững trước các kỹ thuật bypass nâng cao.
