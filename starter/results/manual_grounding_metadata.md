# Grounding + metadata — 5 câu test × top-3 (chấm thủ công)

Grounding: 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh; 2 = đủ để trả lời và truy nguồn. Metadata: kiểm tra `source`, `page`, `section` so với PDF; cột *auto* chỉ là kiểm tra sơ bộ, không thay nhãn thủ công.

## Cấu hình A

### t01 — Số liệu về tình hình ứng dụng TMĐT trong doanh nghiệp được tổng hợp từ khảo sát bao nhiêu doanh nghiệp và theo hình thức nào?
- Đáp án kỳ vọng: 5.531 doanh nghiệp, hình thức điền phiếu trực tiếp (không nhầm với con số 'gần 7.500 doanh nghiệp' ở Lời giới thiệu).
- Gold page: [54] | filter: {'section': 'chuong_4'} | auto Hit@1=False Hit@3=False
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p055:A00` score=0.8331 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=55 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
3. Quy mô của doanh nghiệp tham gia khảo sát
12%
Doanh nghiệp vừ a và nhỏ
Doanh nghiệp lớn
88%
II. MỨC ĐỘ SẴN SÀNG ỨNG DỤNG TMĐT CỦA DOANH NGHIỆP
1. Hạ tầng công nghệ thông tin
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng
57%
47%
31% | 33%28%29%
2022
22% | 20% | 2023
Quản lý nhân sự | Quản lý chuỗi | Quản lý chăm sóc | Quản trị
cung ứng | khách hàng | doanh nghiệp

[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp tham gia khảo sát)

[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
```

2. `sach-trang-tmdt-2023:p059:A00` score=0.7676 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=59 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
1.4. Doanh nghiệp tham gia kinh doanh trên sàn giao dịch TMĐT và mạng xã hội14
65%
58%
2022
23% | 23% | 2023
Doanh nghiệp kinh doanh | Doanh nghiệp kinh doanh
trên sàn giao dịch TMĐT | trên mạng xã hội
2. Thương mại điện tử trên nền tảng di động
2.1. Doanh nghiệp có website phiên bản di động và ứng dụng kinh doanh di động
18% | Doanh nghiệp có website phiên bản di động
19% | Doanh nghiệp có ứng dụng kinh doanh di động
Doanh nghiệp cho phép người mua thực hiện toàn bộ
41% | quá trình mua sắm
```

3. `sach-trang-tmdt-2023:p061:A00` score=0.7651 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=61 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp
63%
25%
7% | 2% | 3%
Dưới 10 triệu | Từ 10 - 20 | Từ 20- 50 | Trên 50 - 100 | Trên 100
đồng | triệu đồng | triệu đồng | triệu đồng | triệu đồng
2. Tình hình vận hành website, ứng dụng di động TMĐT
2.1. Đánh giá của doanh nghiệp về mức độ hiệu quả của các hình thức bán hàng
Qua ứng dụng di động | 25% | 52% | 23%
Qua website của doanh nghiệp | 23% | 53% | 24%
Qua sàn giao dịch TMĐT | 26% | 51% | 24%
Qua mạng xã hội | 16% | 50% | 34%
```

### t02 — Nền tảng số trung gian có bắt buộc hiển thị mọi phản hồi, đánh giá của người tiêu dùng không? Có trường hợp nào được loại trừ?
- Đáp án kỳ vọng: Phải hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản hồi, đánh giá vi phạm quy định pháp luật hoặc trái đạo đức xã hội.
- Gold page: [11] | filter: None | auto Hit@1=False Hit@3=False
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p012:A00` score=0.7852 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=12 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
7
9
11
13
Chỉ định, công bố công khai đầu mối tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD liên quan đến sản phẩm, hàng hóa, dịch vụ, nội dung thông
tin trên nền tảng số trung gian; tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD đối với tổ chức thiết lập, vận hành nền tảng số trung gian;
Trực tiếp lưu trữ thông tin hoặc cung cấp giải pháp lưu trữ thông tin về sản
phẩm, hàng hóa, dịch vụ và các giao dịch liên quan, cho phép NTD truy cập,
truy vết, tải, lưu trữ và in
```

2. `sach-trang-tmdt-2023:p012:A01` score=0.7838 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=12 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
phép NTD truy cập,
truy vết, tải, lưu trữ và in hóa đơn, chứng từ, tài liệu liên quan đến giao dịch
trên nền tảng số trung gian mà mình quản lý;
Cung cấp báo cáo về các hoạt động kiểm duyệt nội dung đã thực hiện theo
yêu cầu của cơ quan nhà nước có thẩm quyền;
Xác thực danh tính tổ chức, cá nhân bán sản phẩm, hàng hóa, cung cấp dịch
vụ trên nền tảng số của mình;
8
10
12
14
Có biện pháp cho phép hiển thị ưu tiên đánh giá, phản ánh, kiến nghị của
tổ chức xã hội tham gia BVQLNTD hoặc tổ chức đánh
```

3. `sach-trang-tmdt-2023:p011:A02` score=0.7581 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
phẩm, hàng hóa, dịch vụ do tổ
chức, cá nhân kinh doanh bán, cung cấp, bao gồm các nội dung bắt buộc thể
hiện trên nhãn hàng hóa theo quy định của pháp luật về nhãn hàng hóa, trừ
các thông tin có tính chất riêng biệt theo sản phẩm, bao gồm: ngày, tháng,
năm sản xuất; thời hạn sử dụng; số lô sản xuất; số khung, số máy; tiêu chuẩn
kết quả cần đạt được trong cung cấp sản phẩm, hàng hóa, dịch vụ;
Cung cấp thông tin về tổ chức, cá nhân kinh doanh hoạt động trên nền tảng
số trung gian khi NTD giao
```

### t03 — Theo Luật Giao dịch điện tử (sửa đổi), điều gì phân biệt một nền tảng số trung gian với các nền tảng số phục vụ giao dịch điện tử khác?
- Đáp án kỳ vọng: Chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
- Gold page: [17] | filter: None | auto Hit@1=False Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p017:A00` score=0.8218 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=17 section=`chuong_1` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
Hệ thống thông tin phục vụ giao dịch điện tử là tập hợp phần cứng, phần mềm và
cơ sở dữ liệu được thiết lập với chức năng, tính năng chính để phục vụ giao dịch
điện tử, bảo đảm xác thực, tin cậy trong giao dịch điện tử.
Nền tảng số phục vụ giao dịch điện tử là hệ thống thông tin quy định tại khoản 1
Điều 45 Luật này tạo môi trường điện tử cho phép các bên thực hiện giao dịch hoặc
cung cấp, sử dụng sản phẩm, dịch vụ hoặc sử dụng để phát triển sản phẩm, dịch vụ.
Nền tảng số trung gian phục vụ
```

2. `sach-trang-tmdt-2023:p017:A01` score=0.8171 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=17 section=`chuong_1` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
sản phẩm, dịch vụ.
Nền tảng số trung gian phục vụ giao dịch điện tử là nền tảng số phục vụ giao dịch
điện tử mà chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
HỆ THỐNG THÔNG TIN
PHỤC VỤ GIAO DỊCH ĐIỆN TỬ
1
2
Định nghĩa hệ thống tin phục vụ giao dịch điện tử
Nền tảng số
1
2
```

3. `sach-trang-tmdt-2023:p011:A03` score=0.7901 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
hoạt động trên nền tảng
số trung gian khi NTD giao dịch với tổ chức, cá nhân kinh doanh đó có yêu cầu;
```

### t04 — Danh sách nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT được tổng hợp từ báo cáo của bao nhiêu doanh nghiệp và cho năm hoạt động nào?
- Đáp án kỳ vọng: Từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp cung cấp dịch vụ TMĐT (không nhầm với 2.030 doanh nghiệp của danh sách website bán hàng).
- Gold page: [83] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p083:A00` score=0.8341 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
4. Thị phần dịch vụ TMĐT 18
4.1. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT
18 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp CCDVTMĐT gửi về Bộ Công Thương.
STT Website/ứng dụng Tên doanh nghiệp
1 Baemin Công ty TNHH Woowa Brothers Việt Nam
2 Be Công ty Cổ phần BE GROUP
3 GoJek Công ty Cổ phần Thương mại Công nghệ Go Viet
4 Grab Công ty TNHH Grab
5 Lazada Công ty TNHH Recess
6 Shopee Công ty TNHH Shopee
7 ShopeeFood Công ty Cổ phần Foody
```

2. `sach-trang-tmdt-2023:p078:A02` score=0.8088 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=78 section=`chuong_5` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
Nam
15 | Telio | Công ty TNHH Telio Việt Nam
16 | thegioididong.com | Công ty Cổ phần Thế Giới Di Động
17 | ushop.unicity.com | Công ty TNHH Unicity Marketing Việt Nam
18 | viettelpost.com.vn | Tổng Công ty Cổ phần Bưu Chính Viettel
19 | vn.myherbalife.com | Công ty TNHH MTV Herbalife Việt Nam
20 | wework.com | Công ty TNHH WeWork Việt Nam
16 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 2.030 doanh nghiệp gửi về Bộ Công Thương.
```

3. `sach-trang-tmdt-2023:p083:A01` score=0.8041 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
ty TNHH Shopee
7 ShopeeFood Công ty Cổ phần Foody
8 Tiki Công ty TNHH TI KI
9 TIKTOK TIKTOK PTE. LTD.
10 Traveloka Công ty TNHH Traveloka Việt Nam
4.2. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT bán buôn bán lẻ
STT Website/ứng dụng Tên doanh nghiệp
1 Lazada Công ty TNHH Recess
2 samsung.com.vn Công Ty TNHH Điện Tử Samsung Vina
3 Selly Công ty TNHH Selly
4 Sendo Công ty Cổ Phần Công Nghệ Sen Đỏ
5 Shopee Công ty TNHH Shopee
6 thuocsi.vn Công ty TNHH Buymed
7 Tiki Công ty TNHH TI
```

### t05 — Theo bảng cập nhật khung pháp lý, Luật Viễn thông (sửa đổi) được ban hành ngày nào và có hiệu lực từ khi nào?
- Đáp án kỳ vọng: Ban hành ngày 24/11/2023, hiệu lực từ 1/7/2024.
- Gold page: [88] | filter: {'section': 'phu_luc'} | auto Hit@1=False Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p092:A02` score=0.8302 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=92 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
Luật Viễn
thông, Luật
CNTT, Luật
GDĐT, Luật
A TTTM
24/4/2017
Nghị định 49/2017/NĐ-CP sửa đổi, bổ sung Điều 15 của Nghị định số
25/2011/NĐ-CP ngày 06 tháng 4 năm 2011 của Chính phủ quy định chi
tiết và hướng dẫn thi hành một số điều của Luật viễn thông và Điều
30 của Nghị định số 174/2013/NĐ-CP ngày 13 tháng 11 năm 2013 của
Chính phủ quy định xử phạt vi phạm hành chính trong lĩnh vực bưu
chính, viễn thông, công nghệ thông tin và tần số vô tuyến điện
20/3/2017
Nghị định 28/2017/NĐ-CP sửa đổi, bổ
```

2. `sach-trang-tmdt-2023:p088:A00` score=0.8264 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=88 section=`phu_luc` | auto: gold_page=True evidence=True filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
Thời gian
ban hành Luật Trạng thái hiệu lực
24/11/2023 Luật viễn thông (sửa đổi) 1/7/2024
22/6/2023 Luật Giao dịch điện tử (sửa đổi) 01/7/2024
20/6/2023 Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi) 01/7/2024
16/6/2022 Luật sửa đổi, bổ sung một số điều của Luật Sở hữu trí tuệ 01/03/2022
11/01/2022
Luật sửa đổi, bổ sung một số điều của Luật Đầu tư công, Luật Đầu tư
theo phương thức đối tác công tư, Luật Đầu tư, Luật Nhà ở, Luật
```

3. `sach-trang-tmdt-2023:p091:A01` score=0.8174 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=91 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
ngày 06 tháng 4 năm 2011 của Chính phủ quy định
chi tiết và hướng dẫn thi hành một số điều của Luật viễn thông
Luật Viễn
thông
14/11/2013 Nghị định 181/2013/NĐ-CP quy định chi tiết thi hành một số điều của Luật Quảng cáo Hết hiệu lực một phần Luật Quảng cáo
08/11/2013 Nghị định 154/2013/NĐ-CP quy định về khu công nghệ thông tin tập trung Luật CNTT
15/7/2013 Nghị định 72/2013/NĐ-CP của Chính phủ về Quản lý, cung cấp, sử dụng dịch vụ Internet và thông tin trên mạng Luật CNTT
16/5/2013 Nghị định
```

## Cấu hình B

### t01 — Số liệu về tình hình ứng dụng TMĐT trong doanh nghiệp được tổng hợp từ khảo sát bao nhiêu doanh nghiệp và theo hình thức nào?
- Đáp án kỳ vọng: 5.531 doanh nghiệp, hình thức điền phiếu trực tiếp (không nhầm với con số 'gần 7.500 doanh nghiệp' ở Lời giới thiệu).
- Gold page: [54] | filter: {'section': 'chuong_4'} | auto Hit@1=False Hit@3=False
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p055:B00` score=0.8262 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=55 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
3. Quy mô của doanh nghiệp tham gia khảo sát
12%
Doanh nghiệp vừ a và nhỏ
Doanh nghiệp lớn
88%
II. MỨC ĐỘ SẴN SÀNG ỨNG DỤNG TMĐT CỦA DOANH NGHIỆP
1. Hạ tầng công nghệ thông tin
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng
57%
47%
31% | 33%28%29%
2022
22% | 20% | 2023
Quản lý nhân sự | Quản lý chuỗi | Quản lý chăm sóc | Quản trị
cung ứng | khách hàng | doanh nghiệp
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp tham gia khảo sát)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý nhân sự: 2022: 57%; 2023: 47%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý chuỗi cung ứng: 2022: 31%; 2023: 28%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý chăm sóc khách hàng: 2022: 33%; 2023: 29%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản trị doanh nghiệp: 2022: 22%; 2023: 20%
```

2. `sach-trang-tmdt-2023:p061:B01` score=0.7728 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=61 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
2. Tình hình vận hành website, ứng dụng di động TMĐT
2.1. Đánh giá của doanh nghiệp về mức độ hiệu quả của các hình thức bán hàng
Qua ứng dụng di động | 25% | 52% | 23%
Qua website của doanh nghiệp | 23% | 53% | 24%
Qua sàn giao dịch TMĐT | 26% | 51% | 24%
Qua mạng xã hội | 16% | 50% | 34%
(Tỷ lệ doanh nghiệp sở hữu website/ứng dụng di động)
Thấp | Trung bình | Cao
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp sở hữu; website/ứng dụng di động)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Dưới 10 triệu đồng: 63%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Từ 10 - 20 triệu đồng: 25%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Từ 20- 50 triệu đồng: 7%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Trên 50 - 100 triệu đồng: 2%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Trên 100 triệu đồng: 3%
```

3. `sach-trang-tmdt-2023:p062:B01` score=0.7525 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=62 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
2.3.1. Hình thức xuất khẩu qua TMĐT doanh nghiệp sử dụng
53%
47%
Xuất khẩu thông qua | Xuất khẩu thông qua
sàn giao dịch TMĐT | website/ứng dụng tự xây dựng
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp sở hữu; website/ứng dụng di động); (Tỷ lệ doanh nghiệp tham gia; xuất khẩu qua TMĐT)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Việt: 94%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Anh: 24%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Trung: 4%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Ngôn ngữ khác: 3%
```

### t02 — Nền tảng số trung gian có bắt buộc hiển thị mọi phản hồi, đánh giá của người tiêu dùng không? Có trường hợp nào được loại trừ?
- Đáp án kỳ vọng: Phải hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản hồi, đánh giá vi phạm quy định pháp luật hoặc trái đạo đức xã hội.
- Gold page: [11] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p011:B00` score=0.7935 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
3 Trách nhiệm của tổ chức thiết lập, vận hành nền tảng số trung gian với NTD trong giao dịch
trên không gian mạng
1
3
5
2
4
6
Có trách nhiệm thực hiện quy định tại Điều 37 và Điều 38, Mục 2 Chương III
trong trường hợp cung cấp dịch vụ liên tục;
Xây dựng, công bố công khai quy chế hoạt động của nền tảng số trung gian
cho NTD, trong đó phân định rõ trách nhiệm của các bên tham gia giao dịch;
Chỉ định, công bố công khai đầu mối liên hệ, người đại diện được ủy quyền
phối hợp với CQQLNN có thẩm quyền trong việc giải quyết các vấn đề liên
quan đến BVQLNTD;
Cho phép NTD phản hồi, đánh giá về tổ chức, cá nhân kinh doanh, sản phẩm,
hàng hóa, dịch vụ do tổ chức, cá nhân kinh doanh bán, cung cấp, đồng thời
hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản
hồi, đánh giá đó vi phạm quy định của pháp luật, trái đạo đức xã hội;
```

2. `sach-trang-tmdt-2023:p012:B00` score=0.7898 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=12 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
7
9
11
13
Chỉ định, công bố công khai đầu mối tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD liên quan đến sản phẩm, hàng hóa, dịch vụ, nội dung thông
tin trên nền tảng số trung gian; tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD đối với tổ chức thiết lập, vận hành nền tảng số trung gian;
Trực tiếp lưu trữ thông tin hoặc cung cấp giải pháp lưu trữ thông tin về sản
phẩm, hàng hóa, dịch vụ và các giao dịch liên quan, cho phép NTD truy cập,
truy vết, tải, lưu trữ và in hóa đơn, chứng từ, tài liệu liên quan đến giao dịch
trên nền tảng số trung gian mà mình quản lý;
Cung cấp báo cáo về các hoạt động kiểm duyệt nội dung đã thực hiện theo
yêu cầu của cơ quan nhà nước có thẩm quyền;
Xác thực danh tính tổ chức, cá nhân bán sản phẩm, hàng hóa, cung cấp dịch
vụ trên nền tảng số của mình;
8
10
12
14
Có biện pháp cho phép hiển thị ưu tiên đánh giá, phản ánh, kiến nghị của
tổ chức xã hội tham gia BVQLNTD hoặc tổ chức đánh giá tín nhiệm theo quy
định của pháp luật;
Minh bạch hoạt động quảng cáo trên không gian mạng theo quy định của
pháp luật trong trường hợp có hoạt động quảng cáo;
```

3. `sach-trang-tmdt-2023:p011:B01` score=0.7382 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
Hiển thị đầy đủ, minh bạch thông tin sản phẩm, hàng hóa, dịch vụ do tổ
chức, cá nhân kinh doanh bán, cung cấp, bao gồm các nội dung bắt buộc thể
hiện trên nhãn hàng hóa theo quy định của pháp luật về nhãn hàng hóa, trừ
các thông tin có tính chất riêng biệt theo sản phẩm, bao gồm: ngày, tháng,
năm sản xuất; thời hạn sử dụng; số lô sản xuất; số khung, số máy; tiêu chuẩn
kết quả cần đạt được trong cung cấp sản phẩm, hàng hóa, dịch vụ;
Cung cấp thông tin về tổ chức, cá nhân kinh doanh hoạt động trên nền tảng
số trung gian khi NTD giao dịch với tổ chức, cá nhân kinh doanh đó có yêu cầu;
```

### t03 — Theo Luật Giao dịch điện tử (sửa đổi), điều gì phân biệt một nền tảng số trung gian với các nền tảng số phục vụ giao dịch điện tử khác?
- Đáp án kỳ vọng: Chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
- Gold page: [17] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p017:B00` score=0.8374 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=17 section=`chuong_1` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
2. Luật Giao dịch điện tử (sửa đổi)
Hệ thống thông tin phục vụ giao dịch điện tử là tập hợp phần cứng, phần mềm và
cơ sở dữ liệu được thiết lập với chức năng, tính năng chính để phục vụ giao dịch
điện tử, bảo đảm xác thực, tin cậy trong giao dịch điện tử.
Nền tảng số phục vụ giao dịch điện tử là hệ thống thông tin quy định tại khoản 1
Điều 45 Luật này tạo môi trường điện tử cho phép các bên thực hiện giao dịch hoặc
cung cấp, sử dụng sản phẩm, dịch vụ hoặc sử dụng để phát triển sản phẩm, dịch vụ.
Nền tảng số trung gian phục vụ giao dịch điện tử là nền tảng số phục vụ giao dịch
điện tử mà chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
HỆ THỐNG THÔNG TIN
PHỤC VỤ GIAO DỊCH ĐIỆN TỬ
1
2
Định nghĩa hệ thống tin phục vụ giao dịch điện tử
Nền tảng số
1
2
```

2. `sach-trang-tmdt-2023:p018:B01` score=0.8026 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=18 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
2. Luật Giao dịch điện tử (sửa đổi)
3
4
Trách nhiệm của chủ quản hệ thống thông tin phục vụ giao dịch điện tử
Trách nhiệm của chủ quản nền tảng số trung gian quy mô rất lớn phục vụ giao dịch điện tử
1
1
2
2
3
3
4
Giám sát an toàn hệ thống thông tin phục vụ giao dịch điện tử của mình theo quy
định của pháp luật về an toàn thông tin mạng.
```

3. `sach-trang-tmdt-2023:p011:B00` score=0.7979 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
3 Trách nhiệm của tổ chức thiết lập, vận hành nền tảng số trung gian với NTD trong giao dịch
trên không gian mạng
1
3
5
2
4
6
Có trách nhiệm thực hiện quy định tại Điều 37 và Điều 38, Mục 2 Chương III
trong trường hợp cung cấp dịch vụ liên tục;
Xây dựng, công bố công khai quy chế hoạt động của nền tảng số trung gian
cho NTD, trong đó phân định rõ trách nhiệm của các bên tham gia giao dịch;
Chỉ định, công bố công khai đầu mối liên hệ, người đại diện được ủy quyền
phối hợp với CQQLNN có thẩm quyền trong việc giải quyết các vấn đề liên
quan đến BVQLNTD;
Cho phép NTD phản hồi, đánh giá về tổ chức, cá nhân kinh doanh, sản phẩm,
hàng hóa, dịch vụ do tổ chức, cá nhân kinh doanh bán, cung cấp, đồng thời
hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản
hồi, đánh giá đó vi phạm quy định của pháp luật, trái đạo đức xã hội;
```

### t04 — Danh sách nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT được tổng hợp từ báo cáo của bao nhiêu doanh nghiệp và cho năm hoạt động nào?
- Đáp án kỳ vọng: Từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp cung cấp dịch vụ TMĐT (không nhầm với 2.030 doanh nghiệp của danh sách website bán hàng).
- Gold page: [83] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p083:B00` score=0.834 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
4. Thị phần dịch vụ TMĐT 18
4.1. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT
18 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp CCDVTMĐT gửi về Bộ Công Thương.
STT Website/ứng dụng Tên doanh nghiệp
1 Baemin Công ty TNHH Woowa Brothers Việt Nam
2 Be Công ty Cổ phần BE GROUP
3 GoJek Công ty Cổ phần Thương mại Công nghệ Go Viet
4 Grab Công ty TNHH Grab
5 Lazada Công ty TNHH Recess
6 Shopee Công ty TNHH Shopee
7 ShopeeFood Công ty Cổ phần Foody
8 Tiki Công ty TNHH TI KI
9 TIKTOK TIKTOK PTE. LTD.
10 Traveloka Công ty TNHH Traveloka Việt Nam
```

2. `sach-trang-tmdt-2023:p083:B01` score=0.8135 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
4.2. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT bán buôn bán lẻ
STT Website/ứng dụng Tên doanh nghiệp
1 Lazada Công ty TNHH Recess
2 samsung.com.vn Công Ty TNHH Điện Tử Samsung Vina
3 Selly Công ty TNHH Selly
4 Sendo Công ty Cổ Phần Công Nghệ Sen Đỏ
5 Shopee Công ty TNHH Shopee
6 thuocsi.vn Công ty TNHH Buymed
7 Tiki Công ty TNHH TI KI
8 TIKTOK TIKTOK PTE. LTD.
9 VinShop Công ty cổ phần One Mount Distribution
10 Voso Công ty TNHH MTV Thương mại Điện tử Bưu Chính VIETTEL
```

3. `sach-trang-tmdt-2023:p078:B02` score=0.786 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=78 section=`chuong_5` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
4.1. Danh sách website TMĐT bán hàng có chức năng đặt hàng trực tuyến dẫn đầu về doanh thu
18 | viettelpost.com.vn | Tổng Công ty Cổ phần Bưu Chính Viettel
19 | vn.myherbalife.com | Công ty TNHH MTV Herbalife Việt Nam
20 | wework.com | Công ty TNHH WeWork Việt Nam
16 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 2.030 doanh nghiệp gửi về Bộ Công Thương.
```

### t05 — Theo bảng cập nhật khung pháp lý, Luật Viễn thông (sửa đổi) được ban hành ngày nào và có hiệu lực từ khi nào?
- Đáp án kỳ vọng: Ban hành ngày 24/11/2023, hiệu lực từ 1/7/2024.
- Gold page: [88] | filter: {'section': 'phu_luc'} | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p088:B01` score=0.8181 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=88 section=`phu_luc` | auto: gold_page=True evidence=True filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
Thời gian
ban hành Luật Trạng thái hiệu lực
24/11/2023 Luật viễn thông (sửa đổi) 1/7/2024
22/6/2023 Luật Giao dịch điện tử (sửa đổi) 01/7/2024
20/6/2023 Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi) 01/7/2024
16/6/2022 Luật sửa đổi, bổ sung một số điều của Luật Sở hữu trí tuệ 01/03/2022
11/01/2022
Luật sửa đổi, bổ sung một số điều của Luật Đầu tư công, Luật Đầu tư
theo phương thức đối tác công tư, Luật Đầu tư, Luật Nhà ở, Luật Đấu
thầu, Luật Điện lực, Luật Doanh nghiệp, Luật Thuế tiêu thụ đặc biệt và
Luật Thi hành án dân sự
01/03/2022
18/06/2020 Luật Đầu tư Hết hiệu lực một phần
17/06/2020 Luật Doanh nghiệp Hết hiệu lực một phần
14/6/2019 Luật Phòng, Chống tác hại của rượu, bia (PCTHRB)
14/6/2019 Luật Thi hành án hình sự
13/6/2019 Luật Quản lý Thuế
12/6/2018 Luật An ninh mạng
12/06/2018 Luật Cạnh tranh
20/6/2017 Luật Sửa đổi, bổ sung một số điều của Bộ Luật hình sự
12/6/2017 Luật Quản lý ngoại thương (QLNT)
12/6/2017 Luật Hỗ trợ doanh nghiệp nhỏ và vừa Hết hiệu lực một phần
```

2. `sach-trang-tmdt-2023:p090:B02` score=0.8069 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=90 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
tiết và hướng dẫn thi hành một số điều của Luật viễn thông và Điều
30 của Nghị định số 174/2013/NĐ-CP ngày 13 tháng 11 năm 2013 của
Chính phủ quy định xử phạt vi phạm hành chính trong lĩnh vực bưu
chính, viễn thông, công nghệ thông tin và tần số vô tuyến điện
Luật Viễn
thông
24/12/2016 Nghị định 166/2016/NĐ-CP quy định về giao dịch điện tử trong lĩnh vực bảo hiểm xã hội, bảo hiểm y tế và bảo hiểm thất nghiệp Hết hiệu lực một phần
```

3. `sach-trang-tmdt-2023:p092:B00` score=0.8029 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=92 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
27/01/2022
Nghị định 14/2022/NĐ-CP sửa đổi bổ sung một số điều của Nghị định
số 15/2020/NĐ-CP ngày 03 tháng 02 năm 2020 của Chính phủ quy
định xử phạt vi phạm hành chính trong lĩnh vực bưu chính viễn thông
tần số vô tuyến điện công nghệ thông tin và giao dịch điện tử và NĐ
119/2020/NĐ-CP ngày 07 tháng 10 năm 2020
27/01/2022
26/8/2020
Nghị định số 98/2020/NĐ-CP quy định xử phạt vi phạm hành chính
trong hoạt động thương mại, sản xuất, buôn bán hàng giả, hàng cấm
và bảo vệ quyền lợi người tiêu dùng
18/5/2020
Nghị định 54/2020/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định
số 127/2015/NĐ-CP ngày 14 tháng 12 năm 2015 của Chính phủ về tổ
chức và hoạt động thanh tra ngành Công Thương
07/7/2020
03/02/2020
Nghị định 15/2020/NĐ-CP quy định về xử phạt hành chính trong lĩnh
vực bưu chính, viễn thông, tần số vô tuyến điện, công nghệ thông tin
và giao dịch điện tử
Hết hiệu lực một
phần
Luật Viễn
thông, Luật
CNTT, Luật
GDĐT, Luật
A TTTM
24/4/2017
```

## Cấu hình C

### t01 — Số liệu về tình hình ứng dụng TMĐT trong doanh nghiệp được tổng hợp từ khảo sát bao nhiêu doanh nghiệp và theo hình thức nào?
- Đáp án kỳ vọng: 5.531 doanh nghiệp, hình thức điền phiếu trực tiếp (không nhầm với con số 'gần 7.500 doanh nghiệp' ở Lời giới thiệu).
- Gold page: [54] | filter: {'section': 'chuong_4'} | auto Hit@1=False Hit@3=False
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p055:B00` score=0.8262 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=55 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
3. Quy mô của doanh nghiệp tham gia khảo sát
12%
Doanh nghiệp vừ a và nhỏ
Doanh nghiệp lớn
88%
II. MỨC ĐỘ SẴN SÀNG ỨNG DỤNG TMĐT CỦA DOANH NGHIỆP
1. Hạ tầng công nghệ thông tin
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng
57%
47%
31% | 33%28%29%
2022
22% | 20% | 2023
Quản lý nhân sự | Quản lý chuỗi | Quản lý chăm sóc | Quản trị
cung ứng | khách hàng | doanh nghiệp
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp tham gia khảo sát)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý nhân sự: 2022: 57%; 2023: 47%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý chuỗi cung ứng: 2022: 31%; 2023: 28%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản lý chăm sóc khách hàng: 2022: 33%; 2023: 29%
1.1. Các phần mềm phổ biến được doanh nghiệp sử dụng — Quản trị doanh nghiệp: 2022: 22%; 2023: 20%
```

2. `sach-trang-tmdt-2023:p061:B01` score=0.7728 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=61 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
2. Tình hình vận hành website, ứng dụng di động TMĐT
2.1. Đánh giá của doanh nghiệp về mức độ hiệu quả của các hình thức bán hàng
Qua ứng dụng di động | 25% | 52% | 23%
Qua website của doanh nghiệp | 23% | 53% | 24%
Qua sàn giao dịch TMĐT | 26% | 51% | 24%
Qua mạng xã hội | 16% | 50% | 34%
(Tỷ lệ doanh nghiệp sở hữu website/ứng dụng di động)
Thấp | Trung bình | Cao
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp sở hữu; website/ứng dụng di động)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Dưới 10 triệu đồng: 63%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Từ 10 - 20 triệu đồng: 25%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Từ 20- 50 triệu đồng: 7%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Trên 50 - 100 triệu đồng: 2%
1.2. . Ước tính chi phí quảng cáo trung bình của doanh nghiệp — Trên 100 triệu đồng: 3%
```

3. `sach-trang-tmdt-2023:p062:B01` score=0.7525 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=62 section=`chuong_4` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
2.3.1. Hình thức xuất khẩu qua TMĐT doanh nghiệp sử dụng
53%
47%
Xuất khẩu thông qua | Xuất khẩu thông qua
sàn giao dịch TMĐT | website/ứng dụng tự xây dựng
[Tiêu đề trục dọc] (Tỷ lệ doanh nghiệp sở hữu; website/ứng dụng di động); (Tỷ lệ doanh nghiệp tham gia; xuất khẩu qua TMĐT)
[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Việt: 94%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Anh: 24%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Tiếng Trung: 4%
2.2. Ngôn ngữ hiển thị trên website, ứng dụng TMĐT — Ngôn ngữ khác: 3%
```

### t02 — Nền tảng số trung gian có bắt buộc hiển thị mọi phản hồi, đánh giá của người tiêu dùng không? Có trường hợp nào được loại trừ?
- Đáp án kỳ vọng: Phải hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản hồi, đánh giá vi phạm quy định pháp luật hoặc trái đạo đức xã hội.
- Gold page: [11] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p011:B00` score=0.7935 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
3 Trách nhiệm của tổ chức thiết lập, vận hành nền tảng số trung gian với NTD trong giao dịch
trên không gian mạng
1
3
5
2
4
6
Có trách nhiệm thực hiện quy định tại Điều 37 và Điều 38, Mục 2 Chương III
trong trường hợp cung cấp dịch vụ liên tục;
Xây dựng, công bố công khai quy chế hoạt động của nền tảng số trung gian
cho NTD, trong đó phân định rõ trách nhiệm của các bên tham gia giao dịch;
Chỉ định, công bố công khai đầu mối liên hệ, người đại diện được ủy quyền
phối hợp với CQQLNN có thẩm quyền trong việc giải quyết các vấn đề liên
quan đến BVQLNTD;
Cho phép NTD phản hồi, đánh giá về tổ chức, cá nhân kinh doanh, sản phẩm,
hàng hóa, dịch vụ do tổ chức, cá nhân kinh doanh bán, cung cấp, đồng thời
hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản
hồi, đánh giá đó vi phạm quy định của pháp luật, trái đạo đức xã hội;
```

2. `sach-trang-tmdt-2023:p012:B00` score=0.7898 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=12 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
7
9
11
13
Chỉ định, công bố công khai đầu mối tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD liên quan đến sản phẩm, hàng hóa, dịch vụ, nội dung thông
tin trên nền tảng số trung gian; tiếp nhận và giải quyết phản ánh, yêu cầu,
khiếu nại của NTD đối với tổ chức thiết lập, vận hành nền tảng số trung gian;
Trực tiếp lưu trữ thông tin hoặc cung cấp giải pháp lưu trữ thông tin về sản
phẩm, hàng hóa, dịch vụ và các giao dịch liên quan, cho phép NTD truy cập,
truy vết, tải, lưu trữ và in hóa đơn, chứng từ, tài liệu liên quan đến giao dịch
trên nền tảng số trung gian mà mình quản lý;
Cung cấp báo cáo về các hoạt động kiểm duyệt nội dung đã thực hiện theo
yêu cầu của cơ quan nhà nước có thẩm quyền;
Xác thực danh tính tổ chức, cá nhân bán sản phẩm, hàng hóa, cung cấp dịch
vụ trên nền tảng số của mình;
8
10
12
14
Có biện pháp cho phép hiển thị ưu tiên đánh giá, phản ánh, kiến nghị của
tổ chức xã hội tham gia BVQLNTD hoặc tổ chức đánh giá tín nhiệm theo quy
định của pháp luật;
Minh bạch hoạt động quảng cáo trên không gian mạng theo quy định của
pháp luật trong trường hợp có hoạt động quảng cáo;
```

3. `sach-trang-tmdt-2023:p011:B01` score=0.7382 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
Hiển thị đầy đủ, minh bạch thông tin sản phẩm, hàng hóa, dịch vụ do tổ
chức, cá nhân kinh doanh bán, cung cấp, bao gồm các nội dung bắt buộc thể
hiện trên nhãn hàng hóa theo quy định của pháp luật về nhãn hàng hóa, trừ
các thông tin có tính chất riêng biệt theo sản phẩm, bao gồm: ngày, tháng,
năm sản xuất; thời hạn sử dụng; số lô sản xuất; số khung, số máy; tiêu chuẩn
kết quả cần đạt được trong cung cấp sản phẩm, hàng hóa, dịch vụ;
Cung cấp thông tin về tổ chức, cá nhân kinh doanh hoạt động trên nền tảng
số trung gian khi NTD giao dịch với tổ chức, cá nhân kinh doanh đó có yêu cầu;
```

### t03 — Theo Luật Giao dịch điện tử (sửa đổi), điều gì phân biệt một nền tảng số trung gian với các nền tảng số phục vụ giao dịch điện tử khác?
- Đáp án kỳ vọng: Chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
- Gold page: [17] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p017:B00` score=0.8374 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=17 section=`chuong_1` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
2. Luật Giao dịch điện tử (sửa đổi)
Hệ thống thông tin phục vụ giao dịch điện tử là tập hợp phần cứng, phần mềm và
cơ sở dữ liệu được thiết lập với chức năng, tính năng chính để phục vụ giao dịch
điện tử, bảo đảm xác thực, tin cậy trong giao dịch điện tử.
Nền tảng số phục vụ giao dịch điện tử là hệ thống thông tin quy định tại khoản 1
Điều 45 Luật này tạo môi trường điện tử cho phép các bên thực hiện giao dịch hoặc
cung cấp, sử dụng sản phẩm, dịch vụ hoặc sử dụng để phát triển sản phẩm, dịch vụ.
Nền tảng số trung gian phục vụ giao dịch điện tử là nền tảng số phục vụ giao dịch
điện tử mà chủ quản nền tảng số độc lập với các bên thực hiện giao dịch.
HỆ THỐNG THÔNG TIN
PHỤC VỤ GIAO DỊCH ĐIỆN TỬ
1
2
Định nghĩa hệ thống tin phục vụ giao dịch điện tử
Nền tảng số
1
2
```

2. `sach-trang-tmdt-2023:p018:B01` score=0.8026 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=18 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
2. Luật Giao dịch điện tử (sửa đổi)
3
4
Trách nhiệm của chủ quản hệ thống thông tin phục vụ giao dịch điện tử
Trách nhiệm của chủ quản nền tảng số trung gian quy mô rất lớn phục vụ giao dịch điện tử
1
1
2
2
3
3
4
Giám sát an toàn hệ thống thông tin phục vụ giao dịch điện tử của mình theo quy
định của pháp luật về an toàn thông tin mạng.
```

3. `sach-trang-tmdt-2023:p011:B00` score=0.7979 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=11 section=`chuong_1` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
1. Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi)
3 Trách nhiệm của tổ chức thiết lập, vận hành nền tảng số trung gian với NTD trong giao dịch
trên không gian mạng
1
3
5
2
4
6
Có trách nhiệm thực hiện quy định tại Điều 37 và Điều 38, Mục 2 Chương III
trong trường hợp cung cấp dịch vụ liên tục;
Xây dựng, công bố công khai quy chế hoạt động của nền tảng số trung gian
cho NTD, trong đó phân định rõ trách nhiệm của các bên tham gia giao dịch;
Chỉ định, công bố công khai đầu mối liên hệ, người đại diện được ủy quyền
phối hợp với CQQLNN có thẩm quyền trong việc giải quyết các vấn đề liên
quan đến BVQLNTD;
Cho phép NTD phản hồi, đánh giá về tổ chức, cá nhân kinh doanh, sản phẩm,
hàng hóa, dịch vụ do tổ chức, cá nhân kinh doanh bán, cung cấp, đồng thời
hiển thị đầy đủ, chính xác kết quả phản hồi, đánh giá, trừ trường hợp phản
hồi, đánh giá đó vi phạm quy định của pháp luật, trái đạo đức xã hội;
```

### t04 — Danh sách nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT được tổng hợp từ báo cáo của bao nhiêu doanh nghiệp và cho năm hoạt động nào?
- Đáp án kỳ vọng: Từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp cung cấp dịch vụ TMĐT (không nhầm với 2.030 doanh nghiệp của danh sách website bán hàng).
- Gold page: [83] | filter: None | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p083:B00` score=0.834 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=True filter_ok=None | Metadata đúng/đủ: __

```text
4. Thị phần dịch vụ TMĐT 18
4.1. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT
18 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 797 doanh nghiệp CCDVTMĐT gửi về Bộ Công Thương.
STT Website/ứng dụng Tên doanh nghiệp
1 Baemin Công ty TNHH Woowa Brothers Việt Nam
2 Be Công ty Cổ phần BE GROUP
3 GoJek Công ty Cổ phần Thương mại Công nghệ Go Viet
4 Grab Công ty TNHH Grab
5 Lazada Công ty TNHH Recess
6 Shopee Công ty TNHH Shopee
7 ShopeeFood Công ty Cổ phần Foody
8 Tiki Công ty TNHH TI KI
9 TIKTOK TIKTOK PTE. LTD.
10 Traveloka Công ty TNHH Traveloka Việt Nam
```

2. `sach-trang-tmdt-2023:p083:B01` score=0.8135 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=83 section=`chuong_5` | auto: gold_page=True evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
4.2. Nhóm doanh nghiệp dẫn đầu thị trường cung cấp dịch vụ TMĐT bán buôn bán lẻ
STT Website/ứng dụng Tên doanh nghiệp
1 Lazada Công ty TNHH Recess
2 samsung.com.vn Công Ty TNHH Điện Tử Samsung Vina
3 Selly Công ty TNHH Selly
4 Sendo Công ty Cổ Phần Công Nghệ Sen Đỏ
5 Shopee Công ty TNHH Shopee
6 thuocsi.vn Công ty TNHH Buymed
7 Tiki Công ty TNHH TI KI
8 TIKTOK TIKTOK PTE. LTD.
9 VinShop Công ty cổ phần One Mount Distribution
10 Voso Công ty TNHH MTV Thương mại Điện tử Bưu Chính VIETTEL
```

3. `sach-trang-tmdt-2023:p078:B02` score=0.786 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=78 section=`chuong_5` | auto: gold_page=False evidence=False filter_ok=None | Metadata đúng/đủ: __

```text
4.1. Danh sách website TMĐT bán hàng có chức năng đặt hàng trực tuyến dẫn đầu về doanh thu
18 | viettelpost.com.vn | Tổng Công ty Cổ phần Bưu Chính Viettel
19 | vn.myherbalife.com | Công ty TNHH MTV Herbalife Việt Nam
20 | wework.com | Công ty TNHH WeWork Việt Nam
16 Dữ liệu được tổng hợp từ báo cáo tình hình hoạt động TMĐT năm 2022 của 2.030 doanh nghiệp gửi về Bộ Công Thương.
```

### t05 — Theo bảng cập nhật khung pháp lý, Luật Viễn thông (sửa đổi) được ban hành ngày nào và có hiệu lực từ khi nào?
- Đáp án kỳ vọng: Ban hành ngày 24/11/2023, hiệu lực từ 1/7/2024.
- Gold page: [88] | filter: {'section': 'phu_luc'} | auto Hit@1=True Hit@3=True
- **Grounding: __ /2 — Lý do: ____**

1. `sach-trang-tmdt-2023:p088:B01` score=0.8181 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=88 section=`phu_luc` | auto: gold_page=True evidence=True filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
Thời gian
ban hành Luật Trạng thái hiệu lực
24/11/2023 Luật viễn thông (sửa đổi) 1/7/2024
22/6/2023 Luật Giao dịch điện tử (sửa đổi) 01/7/2024
20/6/2023 Luật Bảo vệ quyền lợi người tiêu dùng (sửa đổi) 01/7/2024
16/6/2022 Luật sửa đổi, bổ sung một số điều của Luật Sở hữu trí tuệ 01/03/2022
11/01/2022
Luật sửa đổi, bổ sung một số điều của Luật Đầu tư công, Luật Đầu tư
theo phương thức đối tác công tư, Luật Đầu tư, Luật Nhà ở, Luật Đấu
thầu, Luật Điện lực, Luật Doanh nghiệp, Luật Thuế tiêu thụ đặc biệt và
Luật Thi hành án dân sự
01/03/2022
18/06/2020 Luật Đầu tư Hết hiệu lực một phần
17/06/2020 Luật Doanh nghiệp Hết hiệu lực một phần
14/6/2019 Luật Phòng, Chống tác hại của rượu, bia (PCTHRB)
14/6/2019 Luật Thi hành án hình sự
13/6/2019 Luật Quản lý Thuế
12/6/2018 Luật An ninh mạng
12/06/2018 Luật Cạnh tranh
20/6/2017 Luật Sửa đổi, bổ sung một số điều của Bộ Luật hình sự
12/6/2017 Luật Quản lý ngoại thương (QLNT)
12/6/2017 Luật Hỗ trợ doanh nghiệp nhỏ và vừa Hết hiệu lực một phần
```

2. `sach-trang-tmdt-2023:p090:B02` score=0.8069 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=90 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
tiết và hướng dẫn thi hành một số điều của Luật viễn thông và Điều
30 của Nghị định số 174/2013/NĐ-CP ngày 13 tháng 11 năm 2013 của
Chính phủ quy định xử phạt vi phạm hành chính trong lĩnh vực bưu
chính, viễn thông, công nghệ thông tin và tần số vô tuyến điện
Luật Viễn
thông
24/12/2016 Nghị định 166/2016/NĐ-CP quy định về giao dịch điện tử trong lĩnh vực bảo hiểm xã hội, bảo hiểm y tế và bảo hiểm thất nghiệp Hết hiệu lực một phần
```

3. `sach-trang-tmdt-2023:p092:B00` score=0.8029 | source=`data/BCTMDT2023-file-31-1-pdf.pdf` page=92 section=`phu_luc` | auto: gold_page=False evidence=False filter_ok=True | Metadata đúng/đủ: __

```text
PHỤ LỤC: BẢNG CẬP NHẬT KHUNG PHÁP LÝ CƠ BẢN VỀ THƯƠNG MẠI ĐIỆN TỬ
27/01/2022
Nghị định 14/2022/NĐ-CP sửa đổi bổ sung một số điều của Nghị định
số 15/2020/NĐ-CP ngày 03 tháng 02 năm 2020 của Chính phủ quy
định xử phạt vi phạm hành chính trong lĩnh vực bưu chính viễn thông
tần số vô tuyến điện công nghệ thông tin và giao dịch điện tử và NĐ
119/2020/NĐ-CP ngày 07 tháng 10 năm 2020
27/01/2022
26/8/2020
Nghị định số 98/2020/NĐ-CP quy định xử phạt vi phạm hành chính
trong hoạt động thương mại, sản xuất, buôn bán hàng giả, hàng cấm
và bảo vệ quyền lợi người tiêu dùng
18/5/2020
Nghị định 54/2020/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định
số 127/2015/NĐ-CP ngày 14 tháng 12 năm 2015 của Chính phủ về tổ
chức và hoạt động thanh tra ngành Công Thương
07/7/2020
03/02/2020
Nghị định 15/2020/NĐ-CP quy định về xử phạt hành chính trong lĩnh
vực bưu chính, viễn thông, tần số vô tuyến điện, công nghệ thông tin
và giao dịch điện tử
Hết hiệu lực một
phần
Luật Viễn
thông, Luật
CNTT, Luật
GDĐT, Luật
A TTTM
24/4/2017
```
