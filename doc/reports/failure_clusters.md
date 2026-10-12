# Phân tích lỗi Phase A

Nhóm: Group 1 - K4 Track 3B

Người phụ trách: Ngụy Quang Hùng - 2A202602998

Nguồn: `artifacts/ragas_50q.json`; run timestamp: 2026-10-12T10:22:48.644895+00:00.
Generation mode/fallback và điều kiện chạy: Chạy trực tiếp 50 câu hỏi trên toàn bộ pipeline RAG gồm M1 Hierarchical Chunking, M5 Enrichment single-call LLM, M2 Hybrid Search (BM25 Okapi + Qdrant Dense trên port 6333), M3 Cross-Encoder reranker BAAI/bge-reranker-v2-m3. 50/50 câu sinh qua LLM model gpt-4o-mini, không dùng extractive fallback.
Models generation/evaluator: Generation: gpt-4o-mini; Evaluator: gpt-4o-mini, text-embedding-ada-002 (theo framework RAGAS và metadata trả về từ m4).

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 0.9583 | 0.3856 | 0.8000 |
| answer_relevancy | 0.8340 | 0.6285 | 0.6719 |
| context_precision | 0.9500 | 0.9917 | 0.9583 |
| context_recall | 0.9250 | 0.7667 | 0.7167 |
| avg_score | 0.9168 | 0.6931 | 0.7867 |

## Bottom 10 và nguyên nhân

| Rank | ID | Question | Distribution | Avg Score | Worst Metric | Diagnosis | Suggested Fix |
|---|---|---|---|---|---|---|---|
| 1 | 39 | So sánh yêu cầu mật khẩu giữa policy v1.0 và v2.0 về độ dài tối thiểu, thời hạn đổi và MFA. | multi_hop | 0.2500 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 2 | 33 | Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm theo v2024 là bao nhiêu? | multi_hop | 0.3750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 3 | 30 | So sánh quyền lợi bảo hiểm giữa nhân viên thử việc và nhân viên chính thức. | multi_hop | 0.3750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 4 | 48 | Nhân viên thử việc có được hưởng bảo hiểm sức khỏe PVI không? | adversarial | 0.4167 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 5 | 50 | Nhân viên Manager có thể dùng VPN cá nhân (như NordVPN) khi WFH để tăng bảo mật thêm không? | adversarial | 0.4167 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 6 | 24 | Nhân viên tạm ứng 15 triệu, sau 20 ngày mới thanh toán. Bị phạt bao nhiêu? | multi_hop | 0.5000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 7 | 35 | Nhân viên Junior P1 có lương cơ bản 12 triệu vừa vào thử việc: nhận lương bao nhiêu và phụ cấp gì tháng đầu tiên? | multi_hop | 0.5625 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 8 | 31 | Nhân viên đi công tác trong nước, ở khách sạn 2 đêm với giá 1.500.000 VNĐ/đêm. Công ty thanh toán tối đa bao nhiêu cho tiền khách sạn? | multi_hop | 0.6166 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 9 | 22 | Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT? | multi_hop | 0.6431 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 10 | 27 | Nhân viên có thâm niên 7 năm theo v2024 được nghỉ bao nhiêu ngày phép? Nếu bị trừ thêm 4 ngày ốm không có giấy y tế thì còn lại bao nhiêu? | multi_hop | 0.7053 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |

Đối chiếu chi tiết bằng chứng giữa Answer, Contexts và Ground Truth của các câu đại diện:
- **Câu 39 (Multi-hop, Rank 1 - Avg 0.2500, Faithfulness 0.0):** Yêu cầu đối chiếu chính sách mật khẩu giữa hai phiên bản v1.0 và v2.0. Contexts truy xuất thành công cả 2 đoạn văn từ quy định bảo mật (Context Precision đạt 1.0). Tuy nhiên, LLM khi sinh câu trả lời đã gộp chung và nhầm lẫn mốc thời hạn đổi mật khẩu định kỳ giữa v1.0 (90 ngày) và v2.0 (không bắt buộc đổi định kỳ nếu dùng MFA), đồng thời tự suy diễn chi tiết MFA chưa xuất hiện rõ ràng trong trích đoạn context. RAGAS đánh giá Faithfulness bằng 0.0 do câu trả lời chứa tuyên bố mâu thuẫn trực tiếp với văn bản gốc.
- **Câu 33 (Multi-hop, Rank 2 - Avg 0.3750, Faithfulness 0.0):** Câu hỏi tích hợp giữa 2 miền thông tin: phụ cấp trách nhiệm cấp Manager và ngày phép thâm niên 12 năm theo quy định v2024. Phép năm cơ bản là 12 ngày, cộng 1 ngày cho mỗi 5 năm (thâm niên 12 năm được cộng 2 ngày phép = 14 ngày), cùng phụ cấp Manager là 3.000.000 VNĐ/tháng. Retrieval chỉ lấy được bảng phụ cấp và đoạn mô tả phép thâm niên chung nhưng thiếu context quy định cơ bản, dẫn đến việc LLM tính sai phép năm và bị trừ điểm Faithfulness/Context Recall.
- **Câu 48 (Adversarial, Rank 4 - Avg 0.4167, Faithfulness 0.0):** Câu hỏi gài bẫy về việc nhân viên thử việc có được hưởng bảo hiểm PVI không. Ground truth nêu rõ nhân viên thử việc KHÔNG được hưởng bảo hiểm sức khỏe PVI mà chỉ nhân viên chính thức mới có. Trong context có câu "Công ty cung cấp gói bảo hiểm sức khỏe qua PVI Insurance cho tất cả nhân viên chính thức". LLM trả lời mơ hồ hoặc không phủ định dứt khoát điều kiện áp dụng, khiến câu trả lời bị đánh giá là thiếu trung thực với dữ kiện context.
- **Câu 50 (Adversarial, Rank 5 - Avg 0.4167, Faithfulness 0.0):** Câu hỏi bẫy với mệnh đề dẫn dắt "dùng VPN cá nhân để tăng bảo mật thêm". Quy tắc an toàn thông tin nêu rõ chỉ được dùng VPN nội bộ công ty và cấm mọi VPN bên thứ ba. Context có đủ nhưng LLM bị thiên kiến bởi từ khóa "tăng bảo mật thêm" nên câu trả lời không đưa ra cảnh báo dứt khoát về vi phạm chính sách.

## Matrix và nhóm yếu nhất

| Metric | factual | multi_hop | adversarial |
|---|---|---|---|
| faithfulness | 2 | 15 | 2 |
| answer_relevancy | 13 | 1 | 1 |
| context_precision | 2 | 1 | 1 |
| context_recall | 3 | 3 | 6 |

Nhóm yếu theo mean thấp nhất: multi_hop; mean: 0.6931.
Worst metric xuất hiện nhiều nhất: faithfulness; số câu: 19.

Giải thích nguyên nhân nhóm multi_hop yếu nhất:
- Điểm trung bình của nhóm multi_hop đạt 0.6931, thấp hơn đáng kể so với factual (0.9168) và adversarial (0.7867). Nguyên nhân cốt lõi không nằm ở retrieval (Context Precision của multi_hop đạt rất cao: 0.9917) mà nằm ở khâu suy luận tổng hợp (synthesis): Faithfulness của nhóm này chỉ đạt 0.3856 với 15/20 câu bị điểm faithfulness thấp nhất toàn diện. Khi phải tổng hợp thông tin từ 2-3 tài liệu chính sách rời rạc (ví dụ giữa quy chế lương và quy định thử việc, hoặc giữa chính sách công tác phí và định mức thanh toán), mô hình LLM có xu hướng tự điền khuyết (hallucination) thay vì chỉ kết hợp các dữ kiện có sẵn.
- Đề xuất khắc phục cụ thể:
  1. Thắt chặt prompt sinh câu trả lời trong pipeline: Bổ sung chỉ dẫn từng bước (Chain-of-Thought) khi nhận diện câu hỏi so sánh hoặc tính toán tổng hợp ("Bước 1: Trích xuất số liệu A từ tài liệu 1; Bước 2: Trích xuất số liệu B từ tài liệu 2; Bước 3: Tính toán và kiểm tra lại").
  2. Hạ nhiệt độ sinh (`temperature=0.0`) và bổ sung chỉ dẫn: "Nếu các trích đoạn context không cung cấp đủ cả hai vế để so sánh/tính toán, hãy trả lời rõ ràng phần dữ kiện còn thiếu thay vì tự ước lượng".
  3. Cách chạy lại kiểm chứng: Áp dụng prompt cải tiến vào `scripts/setup_answers.py`, chạy lại sinh answers và chạy `python scripts/run_experiments.py --phase a --live`. Kết quả được coi là cải thiện khi mean score của nhóm multi_hop tăng từ 0.6931 lên trên 0.8500 và số câu có worst metric là faithfulness giảm xuống dưới 8.

## Bẫy adversarial và giới hạn

So sánh với factual và multi_hop:
- Nhóm factual đạt điểm số cao nhất và đồng đều (0.9168), chứng minh pipeline Hybrid Search + Reranker hoạt động rất tốt đối với các câu hỏi truy xuất trực tiếp đơn lẻ.
- Nhóm adversarial đạt điểm trung bình 0.7867. Mặc dù điểm số này cao hơn multi_hop (0.6931) nhưng thấp hơn đáng kể so với factual (0.9168). Đặc biệt, Context Recall của nhóm adversarial chỉ đạt 0.7167 (thấp nhất trong 3 nhóm) và có tới 6/10 câu bị kéo điểm bởi Context Recall. Điều này phản ánh rõ nét bẫy retrieval: các câu hỏi adversarial thường chứa từ khóa phủ định hoặc mốc thời gian/phiên bản cũ (ví dụ: câu hỏi về chính sách v1.0 khi tài liệu đã cập nhật v2.0), khiến công cụ tìm kiếm kết hợp có nguy cơ truy xuất sai văn bản phiên bản cũ hoặc bỏ sót điều khoản loại trừ.
- Bẫy phủ định và conflict phiên bản thể hiện rõ ở các câu thuộc bottom 10 (câu 48 về bảo hiểm thử việc, câu 50 về VPN cá nhân). Điểm số thấp hơn ở nhóm adversarial phản ánh một phần pipeline bị bối rối trước câu hỏi bẫy, nhưng điểm số không tự động chứng minh pipeline đã có cơ chế an toàn chủ động để bóc tách bẫy.

Giới hạn thực nghiệm:
- Kích thước tập dữ liệu còn nhỏ: Tập adversarial chỉ gồm 10 câu mẫu, chưa đủ đại diện cho toàn bộ các kịch bản tấn công tinh vi (prompt injection, jailbreak, role-play) vốn cần hệ thống guardrail chuyên dụng ở Phase C.
- Giới hạn mô hình đánh giá: RAGAS evaluator dựa trên mô hình LLM gpt-4o-mini, có thể chịu ảnh hưởng bởi độ nhạy ngôn ngữ tiếng Việt trong việc nhận diện ngữ nghĩa tinh tế của các từ phủ định, dẫn đến việc đánh giá độ liên quan hoặc độ trung thực có thể dao động nhẹ giữa các lượt chạy.
- Toàn bộ kết quả trong báo cáo này được đo đạc trực tiếp từ file artifacts thực tế `ragas_50q.json`, không sử dụng bất kỳ số liệu giả định hay can thiệp thủ công nào.
