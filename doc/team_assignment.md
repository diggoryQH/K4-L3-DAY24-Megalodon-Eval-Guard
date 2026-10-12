# 👥 Phân công Lab K4 Track 3B — 3 người, 0 conflict

---

## 🗂️ Nguyên tắc phân chia

```
Người 1 (A) ──→ src/phase_a_ragas.py   + failure_clusters.md
Người 2 (B) ──→ src/phase_b_judge.py   + bias_report.md
Người 3 (C) ──→ src/phase_c_guard.py   + blueprint.md (tích hợp)
```

> Mỗi người **chỉ sửa file của mình** → merge không conflict.

---

## 📊 Bảng phân công chi tiết

### 👤 Người 1 — Phase A: RAGAS Evaluation (30đ)

| Task | Hàm | Điểm | Mô tả |
|---|---|---|---|
| 1 | `group_by_distribution()` | 5 | Nhóm 50 câu → 20/20/10 |
| 2 | `run_ragas_50q()` | 10 | Chạy RAGAS 4 metrics, trả `RagasEvaluation` |
| 3 | `bottom_10()` | 7 | 10 câu yếu nhất, sắp tăng dần |
| 4 | `cluster_analysis()` | 8 | Matrix worst_metric × distribution |

| File sở hữu | Loại |
|---|---|
| [`src/phase_a_ragas.py`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/src/phase_a_ragas.py) | Code (4 TODO) |
| [`src/m4_eval.py`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/src) | Adapter m4 (đảm bảo `evaluator_models`) |
| [`doc/reports/failure_clusters.md`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/doc/reports/failure_clusters.md) | Report |

**Việc thêm:** Đảm bảo `m4_eval.py` trả đúng `metadata.evaluator_models` (list model IDs thực), viết adapter nếu cần.

---

### 👤 Người 2 — Phase B: LLM Judge (35đ)

| Task | Hàm | Điểm | Mô tả |
|---|---|---|---|
| 5 | `pairwise_judge()` | 10 | LLM chọn A/B/tie, reasoning + scores |
| 6 | `swap_and_average()` | 10 | 2 lượt hoán đổi, consensus |
| 7 | `cohen_kappa()` | 10 | Tính κ từ 10 nhãn |
| 8 | `bias_report()` | 5 | Position + verbosity bias |

| File sở hữu | Loại |
|---|---|
| [`src/phase_b_judge.py`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/src/phase_b_judge.py) | Code (4 TODO) |
| [`doc/reports/bias_report.md`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/doc/reports/bias_report.md) | Report |

**Không sửa file nào khác.** Runner + `judge_binary` helper đã được cung cấp sẵn.

---

### 👤 Người 3 — Phase C: Guardrails + Tích hợp (35đ)

| Task | Hàm | Điểm | Mô tả |
|---|---|---|---|
| 9a | `pii_scan()` | 10 | Presidio detect/anonymize |
| 9b | `check_input_rail()` | 5 | NeMo async input rail |
| 10 | `run_adversarial_suite()` | 10 | 28 inputs qua guard stack |
| 11 | `check_output_rail()` | 5 | NeMo output rail |
| 12 | `measure_p95_latency()` | 5 | Input layers latency ≥20 samples |

| File sở hữu | Loại |
|---|---|
| [`src/phase_c_guard.py`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/src/phase_c_guard.py) | Code (5 TODO) |
| [`doc/reports/blueprint.md`](file:///d:/AI20K/Lab24/K4-Track-3B-Day24-Eval-Guard/doc/reports/blueprint.md) | Report (điền SAU khi có đủ 3 artifacts) |

**Vai trò thêm: Tích hợp cuối** — merge, chạy `check_lab.py`, push repo.

---

## 🚫 Bản đồ file — Ai sửa gì

```
src/
├── phase_a_ragas.py        ← 👤 Người 1 ONLY
├── phase_b_judge.py        ← 👤 Người 2 ONLY
├── phase_c_guard.py        ← 👤 Người 3 ONLY
├── m1_chunking.py          ← 🔒 Chung (copy từ Day18, không sửa)
├── m2_search.py            ← 🔒 Chung
├── m3_rerank.py            ← 🔒 Chung
├── m4_eval.py              ← 👤 Người 1 (adapter nếu cần)
├── m5_enrichment.py        ← 🔒 Chung
├── experiment_support.py   ← 🔒 Không sửa
├── experiment_runners.py   ← 🔒 Không sửa
└── report_contracts.py     ← 🔒 Không sửa

doc/reports/
├── failure_clusters.md     ← 👤 Người 1 ONLY
├── bias_report.md          ← 👤 Người 2 ONLY
└── blueprint.md            ← 👤 Người 3 ONLY

doc/
└── TEAM.md                 ← 👥 Cả 3 (mỗi người điền MỤC INDIVIDUAL riêng)
```

> [!TIP]
> `TEAM.md` — mỗi người chỉ sửa block `### HoVaTen-MSSV` của mình và 1 row trong bảng thành viên. Commit riêng, merge sequential → không conflict.

---

## ⏱️ Timeline trên lớp (tổng ~105 phút)

```
00:00 ─── 15 phút ─── Kiểm tra sẵn sàng (CP0) ──────────────────
                      Cả nhóm xác nhận: env, imports, answers_50q OK
                      
15:00 ─── 30 phút ─── Sprint song song ──────────────────────────
         👤1: code Tasks 1-4     (phase_a_ragas.py)
         👤2: code Tasks 5-8     (phase_b_judge.py)
         👤3: code Tasks 9a-12   (phase_c_guard.py)
         Mỗi người: pytest test_phase_X.py (offline)

45:00 ─── SYNC #1 ────────────────────────────────────────────────
         Merge 3 nhánh vào main
         Chạy: pytest tests/ -m student (tất cả tests)

45:00 ─── 30 phút ─── Chạy live + điền report ───────────────────
         👤1: run --phase a --live → điền failure_clusters.md
         👤2: run --phase b --live → điền bias_report.md
         👤3: run --phase c --live → (chờ artifacts A+B)

75:00 ─── SYNC #2 ────────────────────────────────────────────────
         Merge reports A + B
         👤3: Có đủ 3 artifacts → điền blueprint.md

75:00 ─── 30 phút ─── Đóng gói ──────────────────────────────────
         👤3: Điền blueprint.md từ 3 artifacts
         👥 : Mỗi người điền INDIVIDUAL trong TEAM.md
         👤3: Chạy check_lab.py, fix nếu cần
         
105:00 ── NỘP ────────────────────────────────────────────────────
         👤3 (trưởng nhóm): push + nộp link
```

---

## 🔀 Quy trình Git — Tránh conflict

### Cách 1: Branch riêng (Khuyến nghị)

```bash
# Trước lớp — 1 người setup main
git checkout main
# Copy m1-m5, chạy setup_answers.py, commit

# Trên lớp — mỗi người checkout branch riêng
👤1: git checkout -b feat/phase-a
👤2: git checkout -b feat/phase-b  
👤3: git checkout -b feat/phase-c

# Sau khi code xong — merge sequential (👤3 làm)
git checkout main
git merge feat/phase-a   # không conflict
git merge feat/phase-b   # không conflict (file khác)
git merge feat/phase-c   # không conflict (file khác)
```

### Cách 2: Commit thẳng main (Đơn giản hơn)

```bash
# Vì mỗi người sửa file KHÁC NHAU hoàn toàn
# → có thể commit thẳng main, git pull trước khi push

👤1: sửa phase_a + failure_clusters → commit → push
👤2: git pull → sửa phase_b + bias_report → commit → push
👤3: git pull → sửa phase_c + blueprint → commit → push
```

---

## ✅ Checklist từng người

### 👤 Người 1 — Checklist Phase A

- [ ] `m4_eval.py` có `evaluate_ragas()` trả dict gồm `per_question` + `metadata.evaluator_models`
- [ ] Task 1: `group_by_distribution()` → 3 keys, 20/20/10
- [ ] Task 2: `run_ragas_50q()` → `RagasEvaluation(results, evaluator_models)`
- [ ] Task 3: `bottom_10()` → 10 rows, rank tăng dần, có diagnosis/fix
- [ ] Task 4: `cluster_analysis()` → matrix đúng, nhóm yếu = mean thấp nhất
- [ ] `pytest tests/test_phase_a.py` — pass
- [ ] `run_experiments.py --phase a --live` → `artifacts/ragas_50q.json`
- [ ] Điền `failure_clusters.md` — thay hết `{{...}}`
- [ ] Không còn `# TODO` trong `phase_a_ragas.py`

### 👤 Người 2 — Checklist Phase B

- [ ] Task 5: `pairwise_judge()` → winner/reasoning/scores JSON hợp lệ
- [ ] Task 6: `swap_and_average()` → 2 lượt, convert winner về A/B gốc
- [ ] Task 7: `cohen_kappa()` → κ ∈ [-1, 1]
- [ ] Task 8: `bias_report()` → position/verbosity counts + interpretation
- [ ] `pytest tests/test_phase_b.py` — pass
- [ ] `run_experiments.py --phase b --live` → `artifacts/judge_results.json`
- [ ] Điền `bias_report.md` — thay hết `{{...}}`
- [ ] Không còn `# TODO` trong `phase_b_judge.py`
- [ ] **KHÔNG gửi** `human_label`/`human_note` vào prompt judge

### 👤 Người 3 — Checklist Phase C + Tích hợp

- [ ] Task 9a: `pii_scan()` → detect CCCD/CMND, VN phone, email
- [ ] Task 9b: `check_input_rail()` → dùng `activated_rails`, không keyword match
- [ ] Task 10: `run_adversarial_suite()` → attacks ≥15/20 VÀ clean 8/8
- [ ] Task 11: `check_output_rail()` → sạch giữ nguyên, nhạy cảm thay/redact
- [ ] Task 12: `measure_p95_latency()` → 2 warm-up + ≥20 samples
- [ ] `pytest tests/test_phase_c.py` — pass
- [ ] `run_experiments.py --phase c --live --latency-samples 20` → `artifacts/guard_results.json`
- [ ] Điền `blueprint.md` — latency đã đo + "chưa đo" cho RAG/output/full
- [ ] Không còn `# TODO` trong `phase_c_guard.py`
- [ ] **Tích hợp:** merge tất cả, chạy `check_lab.py`, push

---

## 📦 Việc chung trước lớp (cả nhóm)

| Việc | Ai làm | Ghi chú |
|---|---|---|
| Cài Python 3.11 + C++ Build Tools | Cả 3 | Trên máy mình |
| `pip install -r requirements.txt` | Cả 3 | Kiểm tra imports |
| Copy m1-m5 từ Day 18 | 1 người | Commit vào main |
| `docker compose up -d` (Qdrant) | 1 người | Cần Docker |
| `setup_answers.py --live` | 1 người | Sinh `answers_50q.json`, commit |
| Tạo `.env` với `OPENAI_API_KEY` | Cả 3 | KHÔNG commit |

---

## ⚖️ Cân bằng khối lượng

| Người | Số Tasks | Điểm | Khối lượng code | Report |
|---|---|---|---|---|
| 👤1 (A) | 4 | 30đ | Vừa (+ adapter m4) | failure_clusters.md |
| 👤2 (B) | 4 | 35đ | Vừa (prompt engineering) | bias_report.md |
| 👤3 (C) | 5 | 35đ | Nhiều nhất (async, latency) + tích hợp | blueprint.md |

> [!NOTE]
> Người 3 có nhiều task nhất nhưng code phần lớn là uncomment + sửa nhỏ (hint đã có sẵn trong file).
> Blueprint điền **sau cùng** khi đã có đủ 3 artifacts, nên không chờ đợi lâu.
> Nếu cần cân bằng hơn, Người 1 có thể hỗ trợ Người 3 phần `blueprint.md`.
