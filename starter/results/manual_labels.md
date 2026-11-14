# Nhãn chấm thủ công — coherence, grounding, metadata

**Người chấm và phương pháp:** Claude (Opus 5.5, trong Claude Code) đọc toàn văn chunk/top-3 và đề xuất nhãn kèm lý do. Tác giả (Nguyễn Minh Phương) duyệt từng bảng ngày 2026-11-14 và đồng ý toàn bộ, không sửa nhãn nào. Không dùng LLM judge tự động: mọi nhãn do người đọc trực tiếp văn bản, không suy ra từ Hit@k.

**Nguy cơ thiên lệch:**
- Tác giả kiêm người chấm, và người đề xuất nhãn đã biết kết quả Hit@k trước khi chấm.
- Chỉ có một người chấm, nên không đo được độ đồng thuận.
- Mẫu nhỏ (10 vị trí, 5 câu).

Văn bản đầy đủ của từng chunk được chấm nằm trong `manual_coherence.md` và `manual_grounding_metadata.md`.

## 1. Chunk coherence (10 vị trí × A/B)

**Cách chọn vị trí** (cố định trong code `src/run.py::coherence_positions` trước khi chấm): lấy 10 trang nội dung đầu tiên theo số trang. Ở mỗi trang, vị trí là đoạn đầu tiên không phải heading và dài ≥ 80 ký tự. Chấm chunk chứa vị trí đó. C dùng chung chunk với B nên không chấm riêng.

**Thang điểm:** 0 = bị cắt giữa ý hoặc thiếu chủ thể nên không hiểu; 1 = hiểu một phần, thiếu ngữ cảnh; 2 = tự hiểu được và giữ trọn ý.

| # | Trang | Chunk A | A | Chunk B | B | Lý do |
|---|---|---|---|---|---|---|
| 1 | 3 | p003:A00 | 1 | p003:B00 | 2 | A dừng giữa câu "Trong bức tranh tổng thể về…". B chứa trọn đoạn Lời giới thiệu và kết thúc ở cuối câu. |
| 2 | 10 | p010:A00 | 1 | p010:B00 | 2 | A có đủ ngày thông qua/hiệu lực nhưng kết thúc bằng 2 tiêu đề sơ đồ không kèm nội dung. B chứa trọn mục Luật BVQLNTD, kể cả câu trách nhiệm. |
| 3 | 11 | p011:A00 | 1 | p011:B00 | 2 | A dừng ở "phối hợp với CQQLNN có thẩm". B chứa trọn mục 3, kể cả vế ngoại lệ "trừ trường hợp…". |
| 4 | 12 | p012:A00 | 0 | p012:B00 | 1 | A mở đầu bằng số thứ tự rác "7/9/11/13", không có chủ thể (danh sách nối tiếp từ tr. 11) và dừng giữa câu. B có tên luật nhờ heading được gắn kèm, nhưng vẫn thiếu chủ thể "trách nhiệm của nền tảng số trung gian" vì heading nằm ở tr. 11. |
| 5 | 13 | p013:A00 | 1 | p013:B00 | 2 | A dừng ở "các giải pháp". B chứa trọn mục 4 (nền tảng số lớn). |
| 6 | 14 | p014:A00 | 2 | p014:B00 | 1 | A là cả trang (306 ký tự), đủ ý về Luật GDĐT. B bị gắn nhầm heading "1. Luật BVQLNTD" của trang trước lên trước mục "2. Luật GDĐT", gây hiểu nhầm ngữ cảnh. |
| 7 | 15 | p015:A00 | 0 | p015:B00 | 1 | A có chuỗi số rác ở đầu, hai cột bị xen nhau và dừng giữa câu. B có đủ trang nhưng hai cột "điều kiện kinh doanh" và "trách nhiệm" vẫn xen kẽ (lỗi trích xuất 2 cột). |
| 8 | 16 | p016:A00 | 0 | p016:B00 | 1 | A không có chủ thể và dừng giữa câu. B có tên luật nhưng các cột vẫn xen nhau, khó biết mỗi ý thuộc danh sách nào. |
| 9 | 17 | p017:A00 | 1 | p017:B00 | 2 | A cắt đúng giữa định nghĩa "Nền tảng số trung gian phục vụ…". B chứa trọn các định nghĩa, có tên luật. |
| 10 | 18 | p018:A00 | 1 | p018:B00 | 1 | A dừng ở "Công bố công khai". B giữ câu trọn vẹn nhưng thiếu chủ thể, vì heading "Trách nhiệm của chủ quản…" nằm ở chunk sau. |
| | | **Trung bình** | **0.8/2** (8/20) | | **1.5/2** (15/20) | |

## 2. Grounding quality (5 câu test × top-3)

**Thang điểm:** 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện hoặc ngữ cảnh cần thiết; 2 = đủ để trả lời và truy được nguồn. Đây là đánh giá **bằng chứng truy xuất được**, không phải độ chính xác câu trả lời của LLM.

| Câu | A | B | C | Lý do |
|---|---|---|---|---|
| t01 | 0 | 0 | 0 | Không chunk nào trong top-3 chứa "5.531" hay "điền phiếu trực tiếp". Chú thích cuối tr. 54 không lên top-3; ba cấu hình đều trả về các trang biểu đồ 55/59/61/62 của chương 4. |
| t02 | 0 | 2 | 2 | A: chunk chứa vế ngoại lệ (p011:A01) không lên top-3; chỉ lấy được chunk lân cận nói về nghĩa vụ khác (tr. 12, phần còn lại của tr. 11). B/C: #1 (p011:B00) chứa trọn nghĩa vụ hiển thị và ngoại lệ "trừ trường hợp… vi phạm pháp luật, trái đạo đức xã hội". |
| t03 | 2 | 2 | 2 | Định nghĩa "chủ quản nền tảng số độc lập với các bên thực hiện giao dịch" có trong top-3 (A ở #2, B/C ở #1, kèm tên Luật GDĐT). |
| t04 | 2 | 2 | 2 | #1 chứa "797 doanh nghiệp", "năm 2022" và heading 4.1, nên phân biệt được với danh sách 2.030 doanh nghiệp ở tr. 78. |
| t05 | 2 | 2 | 2 | Dòng bảng "24/11/2023 Luật viễn thông (sửa đổi) 1/7/2024" nằm cùng chunk với tiêu đề cột "Thời gian ban hành / Trạng thái hiệu lực" (A ở #2, B/C ở #1). |
| **Phân bố 0/1/2** | 2/0/3 | 1/0/4 | 1/0/4 | |
| **Trung bình** | **1.2/2** | **1.6/2** | **1.6/2** | |

## 3. Metadata usefulness (5 câu test × top-3 = 15 bản ghi mỗi cấu hình)

Mỗi bản ghi được kiểm tra `document_id`, `source`, `page`, `section` so với PDF (số trang PDF trùng số trang in) và bảng chương trong `data/manifest.json`.

| Cấu hình | Metadata đủ và đúng | Filter tuân thủ@3 (câu test có filter: t01, t05) | Ghi chú |
|---|---|---|---|
| A | 15/15 | 2/2 | Không lọc; tuân thủ do tình cờ (câu hỏi đã nghiêng về đúng chương) |
| B | 15/15 | 2/2 | Không lọc; tuân thủ do tình cờ |
| C | 15/15 | 2/2 | Lọc bằng SQL `WHERE section = …`, tuân thủ được bảo đảm |

**Trường có ích:**
- `page` cho phép mở đúng trang PDF để kiểm chứng (mọi lỗi trong bảng trên đều được truy lại bằng page).
- `section` giúp giới hạn phạm vi. Trên dev, q14 ở B lấy 2 chunk ngoài phạm vi (tr. 61 chương 4, tr. 52 chương 3); ở C, top-3 chỉ còn trang chương 5 (tuân thủ filter dev: B 1/2 → C 2/2).

**Hạn chế:**
- `section` chỉ lọc đúng chương. Nếu bằng chứng không được xếp hạng cao trong chương đó thì lọc cũng không cứu được (t01).
- Trường phụ `heading` của B được mang từ trang trước sang trang sau. Ở tr. 14 heading bị gán nhầm thành "1. Luật BVQLNTD" trong khi nội dung là Luật GDĐT. Trường này không dùng để lọc, nhưng làm giảm coherence (vị trí #6).
