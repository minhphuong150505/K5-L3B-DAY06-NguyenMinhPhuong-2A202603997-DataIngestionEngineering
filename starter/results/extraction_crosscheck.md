# Kiểm chứng mẫu trích xuất text (2026-11-14)

Bộ đọc chính: **pypdf 6.21.4**. Không dùng OCR vì PDF được xuất từ InDesign, đã có lớp text. Đối chiếu với **poppler `pdftotext`** (một bộ đọc độc lập) trên 14 trang mẫu. Các trang này gồm cả những trang bị cảnh báo `missing_fonttools` (19, 30, 31, 34, 77).

Phép đo: tập từ (`\w+`, chữ thường, NFC). Overlap = |từ pypdf ∩ từ poppler| / |từ poppler|.

| Trang | Token pypdf | Token poppler | Overlap | Từ có dấu chỉ poppler có |
|---|---|---|---|---|
| 3 | 458 | 463 | 97,9% | — |
| 10 | 189 | 200 | 95,4% | năm, trắng, việt (header) |
| 19 | 297 | 294 | 91,6% | cuốitin, cụccông, … (poppler dính chữ hai cột) |
| 20 | 484 | 495 | 96,4% | header |
| 22 | 242 | 253 | 91,1% | header |
| 30 | 231 | 243 | 93,5% | header |
| 31 | 215 | 221 | 93,1% | — |
| 34 | 146 | 157 | 94,1% | header |
| 40 | 214 | 225 | 97,7% | header |
| 54 | 252 | 263 | 93,5% | header |
| 75 | 104 | 109 | 93,0% | — |
| 77 | 114 | 119 | 93,4% | — |
| 85 | 179 | 184 | 96,0% | — |
| 88 | 308 | 319 | 95,5% | header |

**Kết luận:**
- Phần chênh lệch là header "SÁCH TRẮNG THƯƠNG MẠI ĐIỆN TỬ VIỆT NAM NĂM 2023" và số trang, vốn bị cố ý loại khi chuẩn hóa. Ngoài ra poppler ghép chữ sai giữa các cột ở tr. 19.
- Không thấy từ tiếng Việt nào bị mất dấu hoặc sai mã ký tự trong pypdf. Cảnh báo `missing_fonttools` chỉ liên quan đến các font số và tiêu đề trên biểu đồ, không làm hỏng text.
- Hạn chế vẫn còn: thứ tự nhãn và số liệu trên các trang biểu đồ bị lệch (xem `known_issues` trong `data/manifest.json`). Cả hai bộ đọc đều gặp lỗi này vì đây là bố cục đồ họa.

# Sửa lỗi trích xuất trên trang biểu đồ (2026-11-14)

**Cách 1: pypdf layout mode** cho 46 trang `chart_heavy`. Các cột thị giác được nối bằng ` | `. Áp dụng tốt cho biểu đồ cột ngang và bảng, ví dụ:

| Trang | Trước | Sau |
|---|---|---|
| 44 | `21% 31% 36% 40% 41% 51% Bảo hành sản phẩm … Nhiều chương trình khuyến mại` | `Nhiều chương trình khuyến mại \| 51%` … `Bảo hành sản phẩm \| 21%` |
| 75 | `Chính sách bảo vệ thông tin cá nhân 91,5% 93,4%` (không rõ cột) | `Chính sách bảo vệ \| 91,5% \| 93,4%` dưới header 2 cột |

**Cách 2: ghép theo toạ độ bằng PyMuPDF 1.26.5** (`src/chart_pairs.py`) cho biểu đồ cột đứng và biểu đồ nhóm:
- Nhãn là chữ ArialMT cỡ ≤ 10,4pt, không đậm. Tiêu đề (MyriadPro-Bold) và chữ xoay dọc bị loại.
- Hàng trục là hàng có ≥ 3 khối nhãn cùng toạ độ y.
- Mỗi giá trị được gán cho nhãn gần nhất theo x, ở hàng trục ngay bên dưới.
- Tên series lấy từ chú thích năm (20xx) nằm trong vùng biểu đồ, theo thứ tự trên → dưới, tương ứng cột trái → phải.
- Chỉ ghi kết quả khi mọi nhãn trong hàng có cùng số giá trị. Trường hợp khác ghi log `chart_pairing_unresolved`.

Kết quả: **112 cặp trên 12 trang**. 3 hàng chưa ghép được (tr. 49, 58, 61).

**Kiểm tra bằng mắt** (render bằng `mutool draw`, so với ảnh gốc), người kiểm tra là tác giả:

| Trang | Biểu đồ | Số cặp | Kết quả |
|---|---|---|---|
| 42 | Phương tiện truy cập Internet; thời gian truy cập (2022/2023) | 16 | Đúng 16/16 (nhãn "Máy tính để bàn / Máy tính xách tay" là một nhãn chung trong bản gốc) |
| 47 | Giao đồ ăn; du lịch; thanh toán | 19 | Đúng 19/19 (text cũ ghép sai "KhácBooking.com"; nay đã tách đúng) |
| 50 | Lý do mua của người bán nước ngoài (2021/2022/2023) | 15 | Đúng 15/15 |
| 51 | Mức độ hài lòng (2022/2023) | 8 | Đúng 8/8 |
| 55 | Phần mềm doanh nghiệp sử dụng (2022/2023) | 8 | Đúng 8/8 |
| 63 | Quốc gia xuất khẩu qua TMĐT | 6 | Đúng 6/6 ("Quốc gia" là đúng nhãn in trong bản gốc) |
| 65 | Tra cứu website cơ quan nhà nước (2022/2023) | 6 | Đúng 6/6 |

Tổng cộng **78/78 cặp đúng** trên 7/12 trang. 5 trang còn lại (46, 61, 62, 66, 69) chưa kiểm tra bằng mắt.

**Hạn chế còn lại:**
- Biểu đồ tròn: chú giải nối với lát cắt bằng màu nên chưa ghép được.
- 3 hàng chưa ghép được ở tr. 49, 58, 61.
- Tr. 35–37 cần OCR.
- Mẫu kiểm tra nhỏ và do tác giả tự chấm.

# OCR cho tr. 35–37 (2026-11-14)

**Vấn đề:** số liệu của 6 biểu đồ e-Conomy SEA (Indonesia, Philippines, Thái Lan, Malaysia, Singapore, Việt Nam) được vẽ thành hình vector, không có lớp text.

**Công cụ:** Tesseract 5.3.4 (CLI, có sẵn gói `vie` và `eng`; chỉ dùng whitelist `0123456789%-,.`), render ảnh bằng PyMuPDF 1.26.5. Code nằm trong `src/ocr_charts.py`.

**Cách làm:**
1. **Hình vẽ PDF quyết định vị trí và nghĩa, OCR chỉ đọc chữ số.**
   - Mỗi con số là một hình màu gần đen, cho biết đúng vị trí và số lượng con số.
   - Cột của mỗi series dùng chung một màu, và màu đó trùng với ô chú giải có chữ bên phải, cho biết series.
   - Vạch xám chân cột cho biết ô cột; nhãn năm cho biết nhóm.
2. Mỗi số được cắt riêng, thêm viền trắng, và OCR **4 lần** (zoom 8× và 12× nhân với `--psm 7` và `8`). Bỏ dấu "," hoặc "." thừa ở cuối. Chấp nhận khi mọi lần đọc không rỗng giống nhau (cần ít nhất 2 lần), hoặc khi ≥3/4 lần khớp. Ngược lại thì bỏ giá trị và ghi log `ocr_value_rejected`.
3. **Dấu âm xác định bằng hình học** (một hình vẽ mảnh nằm bên trái), không dựa vào OCR.

**Kiểm chứng toàn bộ** (không lấy mẫu): so 90 giá trị với gold chép tay từ ảnh render (`results/ocr_gold_p35_37.json`). Chạy lại bằng `.venv/bin/python scripts/check_ocr.py`.

| Phiên bản | Đúng | Sai | Bị từ chối | Ghi chú |
|---|---|---|---|---|
| OCR cả vùng, `psm 11`, 400 DPI | — | — | — | Thiếu nhiều số nhỏ, đọc nhầm số; kết quả thay đổi theo DPI |
| Cắt theo hình vẽ, 2 lần đọc phải khớp | — | 1+ | nhiều | Đọc "58" thành "53" ở cả 2 lần → khớp nhau mà vẫn sai |
| + 4 lần đọc, bỏ "," cuối, dấu âm bằng hình học | 79 | 10 | 1 | 10 lỗi sai đều là đảo series du lịch ↔ nội dung ở tr. 35 (lỗi gán series, không phải OCR) |
| + sửa nhận diện ô chú giải (cột rất thấp bị nhầm là ô chú giải) | **89** | **0** | **1** | Từ chối: Singapore 2023 "-3%", số bị đường biểu đồ đè lên |

**Giới hạn:**
- Tham số OCR và quy tắc chấp nhận được chỉnh trên chính 90 giá trị này. Kết quả 89/90 không phải đánh giá trên dữ liệu mới.
- Người chép gold là tác giả.
- Cách này dựa vào cấu trúc hình vẽ riêng của các biểu đồ này, nên không tự động dùng được cho tài liệu khác.
