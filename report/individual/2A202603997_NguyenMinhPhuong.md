# Báo cáo cá nhân — Day 6

- Học viên: Nguyễn Minh Phương · MSSV 2A202603997 · L3B
- Thời điểm chạy kết quả: 2026-11-14 11:17 (+07:00) · Lệnh: `cd starter && python -m src.ingestion && python -m src.run`
- Công cụ AI: Claude Code (Claude Opus 5.5) được dùng để viết code, chạy thí nghiệm, đề xuất nhãn chấm tay và soạn báo cáo. Tác giả kiểm tra kết quả chạy, duyệt từng bảng nhãn và chọn chiến lược.

## Dữ liệu và pipeline

**Chủ đề, nguồn/quyền, số trang và quy tắc tính trang**
- Tài liệu: *Sách trắng Thương mại điện tử Việt Nam năm 2023* do Cục TMĐT và Kinh tế số (Bộ Công Thương) phát hành. PDF 100 trang, số trang PDF trùng số trang in.
- Quyền sử dụng: tài liệu công khai, nhưng tr. 98 ghi bản quyền thuộc Cục TMĐT và KTS và không có giấy phép tái phân phối rõ ràng. Vì vậy repo chỉ ghi URL tải về và sha256 (`data/manifest.json`), không commit file PDF. Dữ liệu chỉ dùng cho mục đích học tập.
- Quy tắc tính trang: tính **81 trang nội dung** (91.765 ký tự sau chuẩn hóa). Loại 19 trang: bìa và trang trắng (1, 2, 38, 86, 97, 99, 100), mục lục và viết tắt (4–8), trang ngăn chương chỉ có tiêu đề (9, 27, 39, 53, 67, 87), trang thông tin xuất bản có tên cá nhân (98). Tr. 35–37 được tính nhờ OCR.

**Chuẩn hóa, lỗi và giới hạn**
- Đọc bằng pypdf 6.21.4. Chuẩn hóa: Unicode NFC, bỏ ký tự vô hình, gộp khoảng trắng trong dòng, giữ xuống dòng (cần cho chunk B), bỏ header/footer lặp ("SÁCH TRẮNG…", "www.idea.gov.vn" và số trang).
- 49 trang nhiều biểu đồ được trích bằng chế độ layout để nhãn và số nằm cùng dòng, nối các cột bằng ` | `.
- Biểu đồ cột đứng: ghép nhãn với giá trị theo toạ độ PyMuPDF, được 112 cặp trên 12 trang. Kiểm tra bằng mắt 7 trang: 78/78 cặp đúng.
- Tr. 35–37: số liệu vẽ bằng vector nên phải OCR bằng Tesseract 5.3.4. Kết quả 89/90 giá trị đúng so với gold chép tay, 1 giá trị bị từ chối. Lưu ý: tham số OCR được chỉnh trên chính 3 trang này.
- Log (`starter/results/ingestion_errors.jsonl`): 0 lỗi error; các cảnh báo gồm 19 `missing_fonttools` (đối chiếu với poppler thấy không làm sai chữ tiếng Việt), 14 cảnh báo pypdf, 6 trang rỗng, 3 hàng biểu đồ chưa ghép được (tr. 49, 58, 61), 1 giá trị OCR bị từ chối.
- **Giới hạn còn lại:**
  - Biểu đồ tròn chưa ghép được chú giải với giá trị.
  - Sơ đồ nhiều cột bị trích xen kẽ cột và để lại số thứ tự rác như "1 / 3 / 5" (tr. 10–18).
  - Nguồn tự mâu thuẫn: tr. 3 ghi "gần 7.500 doanh nghiệp", còn tr. 54 ghi "5.531 doanh nghiệp".

**Embedding, vector store, metric, lệnh chạy và chi phí**
- Embedding: `aisingapore/SEA-LION-E5-Embedding-600M` (fine-tune từ multilingual-e5-large, XLM-RoBERTa), 1024 chiều, tối đa 512 token. Chạy local trên CPU qua sentence-transformers 5.7.0 và torch 2.15.0+cpu.
  - Query dùng prompt `Retrieval` của model; document không dùng prompt; vector chuẩn hóa L2.
  - Mọi chunk đều ≤ 424 token, nên không chunk nào bị cắt khi embed.
- Vector store: PostgreSQL 16.16 + pgvector 0.8.7 (Docker, `127.0.0.1:55433`), bảng `chunks`.
  - Metric cosine, index HNSW nên tìm kiếm là gần đúng (approximate).
  - Khi lọc dùng `hnsw.iterative_scan = relaxed_order` để vẫn đủ top-3.
- Chi phí: **0 USD** (model local).
- Thời gian:
  - Ingestion khoảng 51 s.
  - Embed A 166,9 s và B 212,1 s.
  - Truy vấn 20 câu × 3 cấu hình 24,6 s.
  - Toàn bộ `src.run` 410,9 s (CPU, RAM 15 GB, không GPU).
  - Lần đầu tải model khoảng 2,2 GB.

**Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn**
- Bắt buộc: `document_id`, `source` (đường dẫn PDF), `page` (int, số trang PDF), `chunk_id`.
- Trường lọc `section` (text): một trong `gioi_thieu`, `chuong_1`…`chuong_5`, `phu_luc`. Giá trị lấy từ trang ngăn chương trong PDF và ghi trong manifest, không phải do mình đoán.
  - Lý do chọn: corpus có những con số và chủ đề trùng nhau giữa các chương, ví dụ số doanh nghiệp khảo sát ở tr. 3 và tr. 54, hay luật được nhắc ở chương 1 và ở phụ lục. Vì vậy câu hỏi gắn với một chương cần giới hạn phạm vi.
- Trường phụ: `year` (int, 2023), `language` (`vi`), `chart_heavy` (bool), `heading` (chỉ có ở chunk B).

## Cấu hình và benchmark

**A / B / C**

| | Chunk | Truy xuất |
|---|---|---|
| A | Cửa sổ ký tự cố định 500, overlap 50, cắt lùi về khoảng trắng; mỗi trang chunk riêng → 232 chunk | top-3 cosine, không lọc |
| B | Dựng lại đoạn từ heading đánh số và dấu kết câu; gộp đoạn tới 1000 ký tự (đoạn ngắn < 200 được phép vượt thêm tối đa 200); heading mới mở chunk mới; gắn heading gần nhất vào đầu chunk bắt đầu giữa mục; không vượt trang → 173 chunk | top-3 cosine, không lọc |
| C | **Dùng chung index B** | Như B, chỉ thêm `WHERE section = …` cho 4 câu có filter; 16 câu còn lại chạy giống hệt B |

- A–B chỉ đổi cách chunk; B–C chỉ đổi filter. Cả ba dùng cùng corpus (`pages.jsonl` sha256 `8a34d914…`), cùng model, store, metric và bộ câu hỏi.
- Chỉnh sửa có chủ đích trước khi chạy chính thức: B được sửa hai lỗi phát hiện khi kiểm tra chunk.
  - Dòng số liệu biểu đồ dạng "6.2. … — Khác: 14%" bị nhận nhầm là heading.
  - Đoạn ngắn cuối trang bị tách thành chunk riêng, làm vỡ evidence của q06 (câu **dev**).
  - Không dùng câu test nào để chỉnh.

**Benchmark (≥20 câu)**
- 20 câu trong `benchmark/questions.jsonl`, chia trước khi chạy thành **15 dev (q01–q15) / 5 test (t01–t05)**.
- Loại câu: trực tiếp, diễn đạt lại, điều kiện, ngoại lệ, metadata filter.
- **4 câu filter `section`:** q14 (`chuong_5`), q15 (`phu_luc`) thuộc dev; t01 (`chuong_4`), t05 (`phu_luc`) thuộc test. Giá trị filter là input giả định người dùng cung cấp trước khi truy xuất, không lấy từ gold.
- Kiểm chứng evidence: mỗi `evidence_quote` phải là chuỗi con của text trang gold sau chuẩn hóa. Kết quả 20/20.
  - Sau khi đổi sang chế độ layout, chỉ sửa định dạng evidence của q13, trước khi chạy cấu hình nào.
  - Nguy cơ rò rỉ dev→test đã ghi ở `benchmark/README.md`: q15/t05 cùng bảng phụ lục; q02/t02 và q03–q04/t03 cùng mục luật.

**Tiêu chí chọn chiến lược**
- **Ghi nhận trung thực:** tiêu chí **không** được ghi lại trước khi xem kết quả test. Kết quả test đã được in cùng dev trong lần chạy đầu tiên. Không có tham số nào được chỉnh theo test, nhưng tập test không còn là holdout độc lập hoàn toàn cho bước *chọn*.
- Tiêu chí (ghi sau): chọn trên **dev**, theo thứ tự:
  1. Evidence Hit@3. Chênh lệch ≤ 1 câu trên 15 câu được coi là hoà, vì nằm trong sai số của mẫu nhỏ.
  2. Tuân thủ filter.
  3. Coherence.
  4. Tài nguyên.

## Kết quả

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| A | dev | 9/15 | 14/15 | 232 | embed 166,9 s | 0 |
| A | test | 1/5 | 3/5 | 232 | | 0 |
| B | dev | 9/15 | 13/15 | 173 | embed 212,1 s | 0 |
| B | test | 4/5 | 4/5 | 173 | | 0 |
| C | dev | 9/15 | 13/15 | 173 (index B) | +0 s embed | 0 |
| C | test | 4/5 | 4/5 | 173 (index B) | | 0 |

Truy vấn cả ba cấu hình (20 câu × 3) mất 24,6 s. Nạp lại cùng phiên bản: 0 chunk embed lại, số dòng giữ nguyên (A 232, B 173).

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| A | 0,8 (10) | 15/15 | test 2/2 · dev 1/2 | 2/0/3 · 1,2 |
| B | 1,5 (10) | 15/15 | test 2/2 · dev 1/2 | 1/0/4 · 1,6 |
| C | 1,5 (10, chung chunk B) | 15/15 | test 2/2 · dev 2/2 | 1/0/4 · 1,6 |

**Đường dẫn trace, nhãn và cách chọn mẫu**
- Trace top-3 đầy đủ: `starter/results/traces_{A,B,C}.jsonl`. Bảng kết quả từng câu: `starter/results/run_report.md`. Số liệu đầy đủ: `starter/results/metrics.json`.
- Nhãn và lý do: `starter/results/manual_labels.md`. Văn bản các mẫu đã chấm: `manual_coherence.md`, `manual_grounding_metadata.md`.
- Cách chọn mẫu:
  - Coherence: 10 trang nội dung đầu tiên (tr. 3, 10–18). Ở mỗi trang lấy đoạn đầu tiên không phải heading và dài ≥ 80 ký tự; vị trí được cố định trong code trước khi chấm.
  - Grounding và metadata: 5 câu test × top-3.
- Người chấm: Claude đề xuất nhãn kèm lý do, tác giả đọc và duyệt toàn bộ (không sửa nhãn nào). Một người chấm, đã biết Hit@k trước khi chấm, nên có nguy cơ thiên lệch.
- Định nghĩa hit: chunk thuộc trang gold **và** chứa trọn `evidence_quote` sau chuẩn hóa.

## Phân tích và kết luận

**A–B (đổi cách chunk)**
- Hit@3 tổng bằng nhau (17/20), nhưng các câu trượt khác nhau.
- B tốt hơn ở Hit@1 test (4/5 so với 1/5), coherence (1,5 so với 0,8) và grounding (1,6 so với 1,2).
  - Lợi thế nằm ở câu **điều kiện/ngoại lệ**: q06 (A trượt vì vế "trường hợp thông báo sau 72 giờ…" sang chunk khác) và t02.
- A tốt hơn trên dev Hit@3 (14/15 so với 13/15). Chunk nhỏ, tập trung giúp A trúng các câu tra một con số trong bảng hoặc biểu đồ (q02, q11).
- Về tài nguyên: B ít chunk hơn (173 so với 232) nhưng embed lâu hơn (212 s so với 167 s) vì chunk dài hơn.

**B–C (đổi filter)**
- Hit@k không đổi: các câu filter mà B trúng thì C cũng trúng; t01 trượt ở cả hai.
- Lọc đảm bảo top-3 nằm đúng chương: tuân thủ filter dev tăng từ 1/2 lên 2/2. Ở q14, B lẫn 2 chunk ngoài phạm vi: tr. 61 (chương 4) và tr. 52 (chương 3, trở ngại của *người tiêu dùng*). C chỉ trả về chunk chương 5 (tr. 85, 70, 75).
- Không tốn thêm embedding hay lưu trữ.

**Ví dụ sai**
1. **t01 (test, filter `chuong_4`, gold tr. 54) — trượt ở cả A/B/C.**
   - Evidence "khảo sát 5.531 doanh nghiệp… điền phiếu trực tiếp" là chú thích cuối trang, nằm lẫn giữa các số % của biểu đồ tròn.
   - Top-3 là các trang biểu đồ 55/59/61/62. Lọc theo chương không giúp được, vì lỗi nằm ở xếp hạng *trong* chương.
   - Nếu không lọc, câu này còn có nguy cơ lấy nhầm "gần 7.500 doanh nghiệp" ở tr. 3.
2. **q02 (dev, gold tr. 10) — A trúng ở #1, B trượt (B trả tr. 14, 11, 12).**
   - Chunk B tr. 10 dài 871 ký tự, gộp heading chương "I. CẬP NHẬT…", câu ngày thông qua/hiệu lực, số rác từ sơ đồ và danh sách trách nhiệm. Câu chứa đáp án bị "pha loãng" trong vector.
   - Các chunk Luật BVQLNTD ở trang sau đều mang cùng heading nên cạnh tranh trực tiếp.
3. (Bổ sung) **q11 (dev, gold tr. 40) — tương tự q02.**
   - Dòng bảng "giá trị mua sắm trực tuyến của một người (USD) … 336" nằm trong chunk B 903 ký tự cùng các chú thích về doanh thu B2C.
   - Các trang biểu đồ 48 và 50 nói về "giá trị mua sắm của một người" thắng.

**Chiến lược chọn: C** (chunk theo cấu trúc + lọc `section` khi người dùng chỉ định phạm vi).
- Trên dev, Hit@3 của C kém A 1/15 câu, được coi là hoà theo tiêu chí. Ở các tiêu chí tiếp theo C tốt hơn: tuân thủ filter dev 2/2 so với 1/2, coherence 1,5 so với 0,8.
- Kết quả test (Hit@1 4/5, grounding 1,6) nhất quán với lựa chọn này, nhưng không được dùng để chọn.
- Đánh đổi: C (B) yếu hơn A với câu hỏi tra một ô số trong bảng hoặc biểu đồ dày đặc.
- Điều kiện áp dụng: C hợp với câu hỏi về điều khoản, định nghĩa, điều kiện/ngoại lệ, và khi người dùng chỉ rõ phạm vi chương. Kết luận chỉ đúng với corpus này.

**Hạn chế**
- Mẫu nhỏ: 5 câu test (1 câu = 20%) và 15 câu dev. Chênh lệch giữa các cấu hình chỉ 1–3 câu, không đủ để kết luận tổng quát.
- Tiêu chí chọn được ghi sau khi đã thấy test (xem trên).
- Nhãn chấm tay do một người: Claude đề xuất, tác giả duyệt. Không có người chấm độc lập.
- Hit dựa trên khớp chuỗi trọn evidence. Câu có bằng chứng tương đương diễn đạt khác sẽ bị tính trượt; q03 đã ghi 2 trang gold để giảm vấn đề này.
- Thời gian đo trên một máy CPU, chạy 1 lần, không lặp lại. HNSW là tìm kiếm gần đúng, nhưng với 405 vector thì sai khác so với tìm kiếm chính xác là nhỏ (chưa đo riêng).
- OCR được chỉnh trên chính dữ liệu dùng để kiểm chứng. Biểu đồ tròn và sơ đồ nhiều cột vẫn trích lỗi.

**Nếu làm lại hoặc mở rộng**
- Lọc bỏ số thứ tự rác của sơ đồ ("1 / 3 / 5") và tách cột theo toạ độ trước khi chunk. Đây là nguồn chính làm giảm coherence ở tr. 12, 15, 16.
- Sửa cách mang heading sang trang mới: chỉ mang khi trang mới không có heading cùng cấp (lỗi ở tr. 14).
- Tách chú thích cuối trang (footnote) thành chunk riêng có `section`, để giải quyết t01.
- Thử hybrid dense + BM25 cho câu tra số liệu (q02, q11), chọn tham số trên dev rồi đánh giá trên một **tập test mới** chưa xem.
- Bổ sung `chapter_title`/`law_name` làm trường lọc thứ hai, và mở rộng benchmark lên 40–50 câu.
