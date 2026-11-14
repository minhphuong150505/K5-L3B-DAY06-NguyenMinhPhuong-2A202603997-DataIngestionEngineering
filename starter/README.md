# Pipeline Day 06 · PostgreSQL + pgvector + SEA-LION-E5

Pipeline đã hiện thực: đọc PDF → chuẩn hóa → chunk (A/B) → embedding local → pgvector → truy xuất top-3 cho ba cấu hình A/B/C → chỉ số + trace + phiếu chấm tay.

| Thành phần | Lựa chọn |
|---|---|
| Corpus | Sách trắng TMĐT Việt Nam 2023, `sach-trang-tmdt-2023`, 81/100 trang nội dung (xem `../data/manifest.json`) |
| Đọc PDF | pypdf 6.21.4 (text + layout mode), PyMuPDF 1.26.5 (toạ độ biểu đồ), Tesseract 5.3.4 (OCR tr. 35–37) |
| Embedding | `aisingapore/SEA-LION-E5-Embedding-600M`, local qua sentence-transformers 5.7.0, torch 2.15.0+cpu; 1024 chiều; max 512 token; query dùng prompt `Retrieval`, document không prompt; vector chuẩn hóa L2. Chi phí 0 |
| Vector store | PostgreSQL 16.16 + pgvector 0.8.7 (Docker), bảng `chunks`, index HNSW `vector_cosine_ops` (approximate), `hnsw.iterative_scan = relaxed_order` khi lọc |
| Benchmark | `../benchmark/questions.jsonl` — 20 câu, 15 dev / 5 test, 4 câu filter `section` |

## Cấu trúc

```text
starter/
├── docker-compose.yml, init.sql   # PostgreSQL 16 + pgvector, cổng 127.0.0.1:55433
├── requirements.txt               # dependencies Python
├── scripts/
│   ├── check_setup.py             # kiểm tra kết nối DB + extension
│   ├── check_embedding.py         # smoke test model + pgvector (tự dọn dữ liệu thử)
│   └── check_ocr.py               # so OCR tr. 35–37 với gold chép tay
├── src/
│   ├── ingestion.py               # đọc PDF, chuẩn hóa NFC, bỏ header/footer, metadata section, log lỗi
│   ├── chart_pairs.py, ocr_charts.py  # ghép nhãn–giá trị biểu đồ, OCR biểu đồ vector
│   ├── chunking.py                # A fixed_size, B by_paragraph
│   ├── embeddings.py              # SeaLionEmbedder
│   ├── store.py                   # PgVectorStore: schema, upsert, prune, search + filter
│   ├── evaluation.py              # Hit@1, Evidence Hit@3, filter compliance
│   └── run.py                     # chạy A/B/C, ghi kết quả
└── results/                       # output (xem bảng bên dưới)
```

## 1. Cài đặt

Cần Docker + Compose, Python 3.11–3.14, Tesseract có gói `vie` (`sudo apt install tesseract-ocr tesseract-ocr-vie`), khoảng 3 GB đĩa cho model.

```bash
cd starter
python3 -m venv .venv && source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # bản CPU, nhẹ hơn bản CUDA
pip install -r requirements.txt
cp .env.example .env            # DATABASE_URL + EMBEDDING_MODEL, không cần API key
docker compose -p day6_student_starter up -d --wait
python scripts/check_setup.py   # kỳ vọng: pgvector 0.8.x, "Setup OK"
python -m scripts.check_embedding   # lần đầu tải model ~2.2 GB vào ~/.cache/huggingface
```

## 2. Dữ liệu

File PDF **không được commit** (tài liệu không có giấy phép tái phân phối rõ ràng). Tải về `data/` ở thư mục gốc repo và kiểm tra hash:

```bash
cd ..   # thư mục gốc repo
curl -L -o data/BCTMDT2023-file-31-1-pdf.pdf "https://valoma.vn/wp-content/uploads/2024/05/BCTMDT2023-file-31-1-pdf.pdf"
sha256sum data/BCTMDT2023-file-31-1-pdf.pdf
# 4b7e4a29d5b7f33282f243116d2a2b59f1fb261b8fa76225f7788def2ccb430f
cd starter
```

## 3. Chạy

```bash
python -m src.ingestion   # ~50 s: results/pages.jsonl, ingestion_errors.jsonl, ingestion_summary.json
python -m src.run         # ~7 phút trên CPU: chunk, embed, nạp DB 2 lần (kiểm tra trùng), truy xuất A/B/C
python scripts/check_ocr.py   # tuỳ chọn: kiểm chứng OCR tr. 35–37
```

`src.run` dùng `results/pages.jsonl` làm đầu vào và báo lỗi nếu có ít hơn 30 trang nội dung, nếu benchmark thiếu câu filter, nếu giá trị filter không có trong metadata, hoặc nếu DB/model không hoạt động. Không có fallback sang vector giả.

### Ba cấu hình

| | Chunk | Truy xuất |
|---|---|---|
| A | `fixed_size(size=500, overlap=50)` theo ký tự, mỗi trang riêng | top-3 cosine, không lọc |
| B | `by_paragraph(max_size=1000, min_size=200)`: dựng lại đoạn từ heading đánh số và dấu kết câu, gắn heading gần nhất làm ngữ cảnh, không vượt trang | top-3 cosine, không lọc |
| C | dùng chung index B | như B, thêm `WHERE section = …` **chỉ** với câu có filter (giá trị giả định người dùng cung cấp trước khi truy xuất) |

### Nạp lại và tài liệu thay đổi

- Khoá chính là `(strategy, chunk_id)`, với `chunk_id = <document_id>:p<page>:<strategy><index>`.
- Mỗi lần nạp, hệ thống so `text_hash` (sha256) và chỉ embed lại chunk mới hoặc đã đổi nội dung. Chunk của tài liệu không còn trong lần chunk mới bị xoá bằng `prune()`.
- `src.run` nạp hai lần liên tiếp và kiểm tra rằng lần hai không embed chunk nào và số dòng không đổi (A 232, B 173).

## 4. Kết quả

| File | Nội dung |
|---|---|
| `results/run_report.md` | Bảng chunk/tài nguyên, Hit@1/Hit@3 dev/test, kết quả từng câu |
| `results/metrics.json` | Số liệu đầy đủ, phiên bản thư viện, thời gian, chi phí |
| `results/traces_{A,B,C}.jsonl` | Trace top-3: chunk ID, text, score, metadata, nhãn hit/evidence/filter |
| `results/chunks_{A,B}.jsonl` | Toàn bộ chunk của mỗi index |
| `results/manual_labels.md` | Nhãn coherence, grounding, metadata kèm lý do |
| `results/manual_coherence.md`, `manual_grounding_metadata.md` | Văn bản đầy đủ của các mẫu đã chấm |
| `results/ingestion_*`, `extraction_crosscheck.md`, `ocr_gold_p35_37.json` | Log lỗi và kiểm chứng trích xuất/OCR |

Dừng DB nhưng giữ dữ liệu: `docker compose -p day6_student_starter stop`.
