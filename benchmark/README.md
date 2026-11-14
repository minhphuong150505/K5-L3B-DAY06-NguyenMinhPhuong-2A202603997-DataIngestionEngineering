# Benchmark — Sách trắng TMĐT Việt Nam 2023

- Corpus: `sach-trang-tmdt-2023` = `data/BCTMDT2023-file-31-1-pdf.pdf` (100 trang, số trang PDF trùng số trang in).
- File câu hỏi: `questions.jsonl` — 20 câu, **15 dev (q01–q15) / 5 test (t01–t05)**, chia trước khi chạy thử.
- Loại câu: `truc_tiep`, `dien_dat_lai`, `dieu_kien`, `ngoai_le`, `metadata_filter`.
- Có 4 câu filter: q14, q15 (dev); t01, t05 (test).
- Evidence đã được kiểm chứng tự động: mỗi `evidence_quote` là chuỗi con của text trang gold sau khi trích bằng pypdf 6.21.4 → Unicode NFC → gộp khoảng trắng. Kết quả 20/20 khớp.

## Trường filter `section` (lấy từ trang bìa chương trong PDF)

| Giá trị | Trang | Tiêu đề chương |
|---|---|---|
| `gioi_thieu` | 3 | Lời giới thiệu |
| `chuong_1` | 9–26 | Cập nhật chính sách pháp luật và tình hình quản lý hoạt động TMĐT |
| `chuong_2` | 27–37 | Tổng quan TMĐT thế giới và khu vực Đông Nam Á |
| `chuong_3` | 39–52 | Người tiêu dùng tham gia TMĐT |
| `chuong_4` | 53–66 | Tình hình ứng dụng TMĐT trong doanh nghiệp |
| `chuong_5` | 67–85 | Tình hình hoạt động của website, ứng dụng TMĐT |
| `phu_luc` | 87–96 | Phụ lục: Bảng cập nhật khung pháp lý cơ bản về TMĐT |

Giá trị filter là **input giả định do người dùng cung cấp trước khi truy xuất** (ví dụ người dùng chọn "chỉ tìm trong chương doanh nghiệp"), không lấy từ gold.

## Vì sao các câu filter cần filter

- t01: trang 3 ghi "gần 7.500 doanh nghiệp", còn chương 4 (tr. 54) ghi 5.531 doanh nghiệp → không lọc dễ lấy nhầm số.
- t04 (không filter, câu điều kiện): tr. 78 có 2.030 doanh nghiệp (website bán hàng), tr. 83 có 797 doanh nghiệp (dịch vụ TMĐT) → dễ nhầm.
- q14: chương 3 (tr. 52) cũng có "trở ngại khi mua hàng trực tuyến" của người tiêu dùng.
- q15/t05: luật cũng được nhắc ở chương 1; bảng ngày ban hành/hiệu lực chỉ có ở phụ lục.

## Nguy cơ rò rỉ dev → test

- q15 (tr. 89) và t05 (tr. 88) cùng bảng phụ lục, cùng dạng câu "ngày ban hành/hiệu lực".
- q02 (tr. 10) và t02 (tr. 11) cùng mục Luật BVQLNTD (sửa đổi).
- q03/q04 (tr. 15–16) và t03 (tr. 17) cùng mục Luật Giao dịch điện tử (sửa đổi).
- Không dùng chung trang gold giữa dev và test.

## Ghi chú

- q03: tr. 16 cũng nêu "an toàn thông tin mạng tối thiểu cấp độ 3" (diễn đạt khác) → chấp nhận cả tr. 15 và 16.
- Chủ động **không** dùng câu hỏi trên trang biểu đồ (tr. 28–37, 41–52, 54–66 phần lớn): pypdf trích nhãn và số liệu biểu đồ lệch thứ tự, không xác định được cặp nhãn–giá trị đáng tin.

## Thay đổi sau khi chốt bộ câu hỏi

- 2026-11-14: Ingestion chuyển các trang `chart_heavy` sang chế độ layout của pypdf (nhãn và số cùng dòng, các cột nối bằng ` | `). Vì vậy **chỉ sửa `evidence_quote` của q13** từ "Chính sách bảo vệ thông tin cá nhân 91,5% 93,4%" thành "Chính sách bảo vệ | 91,5% | 93,4% thông tin cá nhân" cho khớp text mới. Không đổi câu hỏi, đáp án, trang gold hay split. Thay đổi này làm **trước** khi chạy bất kỳ cấu hình nào, và áp dụng chung cho A/B/C.
