# Kết quả chạy A/B/C

- Thời điểm: 2026-11-14T11:17:57+07:00
- Model: `aisingapore/SEA-LION-E5-Embedding-600M` (1024 chiều, max 512 token, query prompt `Retrieval`, document không prompt, vector chuẩn hoá L2), chạy local cpu — chi phí 0
- Store: PostgreSQL 16.16 (Debian 16.16-1.pgdg12+1) + pgvector 0.8.7, bảng `chunks`, HNSW cosine (approximate, iterative scan khi lọc)
- Corpus: 81 trang nội dung từ `results/pages.jsonl` (sha256 8a34d9146537…)
- Câu hỏi: 20 (15 dev / 5 test), top-3

## Chunk và tài nguyên

| Index | Chunker | Số chunk | Ký tự min/median/p90/max | Token median/max | >512 token | Embed (s) | Nạp lại: embed/giữ/xoá |
|---|---|---|---|---|---|---|---|
| A | fixed_size(size=500, overlap=50) | 232 | 84/496/499/499 | 132/257 | 0 | 166.93 | 0/232/0 |
| B | by_paragraph(max_size=1000, min_size=200) | 173 | 19/434/1041/1227 | 141/424 | 0 | 212.1 | 0/173/0 |

C dùng lại index B (không tốn thêm embedding/lưu trữ); chỉ khác ở mệnh đề `WHERE section = …`.

## Retrieval accuracy

| Cấu hình | Split | Hit@1 | Evidence Hit@3 | Gold page@3 | Filter tuân thủ@3 | Câu trượt @3 |
|---|---|---|---|---|---|---|
| A | dev | 9/15 | 14/15 | 15/15 | 1/2 | q06 |
| A | test | 1/5 | 3/5 | 4/5 | 2/2 | t01, t02 |
| A | all | 10/20 | 17/20 | 19/20 | 3/4 | q06, t01, t02 |
| B | dev | 9/15 | 13/15 | 13/15 | 1/2 | q02, q11 |
| B | test | 4/5 | 4/5 | 4/5 | 2/2 | t01 |
| B | all | 13/20 | 17/20 | 17/20 | 3/4 | q02, q11, t01 |
| C | dev | 9/15 | 13/15 | 13/15 | 2/2 | q02, q11 |
| C | test | 4/5 | 4/5 | 4/5 | 2/2 | t01 |
| C | all | 13/20 | 17/20 | 17/20 | 4/4 | q02, q11, t01 |

## Từng câu (rank của chunk hit đầu tiên, `-` = không hit trong top-3)

| Câu | Split | Loại | Filter | A | B | C |
|---|---|---|---|---|---|---|
| q01 | dev | truc_tiep |  | 1 (tr. 3,3,40) | 1 (tr. 3,3,40) | 1 (tr. 3,3,40) |
| q02 | dev | truc_tiep |  | 1 (tr. 10,88,92) | - (tr. 14,11,12) | - (tr. 14,11,12) |
| q03 | dev | dien_dat_lai |  | 1 (tr. 15,16,15) | 1 (tr. 15,16,18) | 1 (tr. 15,16,18) |
| q04 | dev | dieu_kien |  | 2 (tr. 16,16,14) | 2 (tr. 16,16,96) | 2 (tr. 16,16,96) |
| q05 | dev | truc_tiep |  | 2 (tr. 19,19,19) | 1 (tr. 19,19,93) | 1 (tr. 19,19,93) |
| q06 | dev | dieu_kien |  | - (tr. 22,24,23) | 1 (tr. 22,23,23) | 1 (tr. 22,23,23) |
| q07 | dev | ngoai_le |  | 2 (tr. 20,20,20) | 1 (tr. 20,20,22) | 1 (tr. 20,20,22) |
| q08 | dev | truc_tiep |  | 1 (tr. 24,24,23) | 1 (tr. 24,22,23) | 1 (tr. 24,22,23) |
| q09 | dev | truc_tiep |  | 1 (tr. 24,93,90) | 1 (tr. 24,25,24) | 1 (tr. 24,25,24) |
| q10 | dev | truc_tiep |  | 1 (tr. 26,3,78) | 2 (tr. 26,26,78) | 2 (tr. 26,26,78) |
| q11 | dev | dien_dat_lai |  | 1 (tr. 40,48,50) | - (tr. 50,48,48) | - (tr. 50,48,48) |
| q12 | dev | dien_dat_lai |  | 2 (tr. 3,41,3) | 2 (tr. 3,41,51) | 2 (tr. 3,41,51) |
| q13 | dev | truc_tiep |  | 1 (tr. 75,76,70) | 1 (tr. 75,70,76) | 1 (tr. 75,70,76) |
| q14 | dev | metadata_filter | section=chuong_5 | 1 (tr. 85,85,52) | 1 (tr. 85,61,52) | 1 (tr. 85,70,75) |
| q15 | dev | metadata_filter | section=phu_luc | 2 (tr. 88,89,89) | 2 (tr. 88,89,89) | 2 (tr. 88,89,89) |
| t01 | test | metadata_filter | section=chuong_4 | - (tr. 55,59,61) | - (tr. 55,61,62) | - (tr. 55,61,62) |
| t02 | test | ngoai_le |  | - (tr. 12,12,11) | 1 (tr. 11,12,11) | 1 (tr. 11,12,11) |
| t03 | test | dien_dat_lai |  | 2 (tr. 17,17,11) | 1 (tr. 17,18,11) | 1 (tr. 17,18,11) |
| t04 | test | dieu_kien |  | 1 (tr. 83,78,83) | 1 (tr. 83,83,78) | 1 (tr. 83,83,78) |
| t05 | test | metadata_filter | section=phu_luc | 2 (tr. 92,88,91) | 1 (tr. 88,90,92) | 1 (tr. 88,90,92) |

Hit = chunk thuộc trang gold **và** chứa trọn `evidence_quote` (sau NFC + gộp khoảng trắng). Coherence, grounding và metadata cần chấm tay trong `manual_coherence.md` và `manual_grounding_metadata.md`.
