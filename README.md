# DDM501 – Thiết kế hệ thống dự báo nhu cầu bán lẻ

**Sinh viên:** Nguyễn Minh Trường · **MSSV:** 25MS13312

**Học phần:** DDM501 – AI in DevOps, DataOps, MLOps

**Bài tập:** Individual Assignment 1 – ML System Design Document

## Tài liệu hoàn chỉnh

- [Báo cáo PDF tiếng Việt](deliverables/tieng_viet/DDM501_Assignment1_25MS13312_Nguyễn_Minh_Trường.pdf)
- [Bản Word chỉnh sửa](deliverables/tieng_viet/DDM501_Assignment1_25MS13312_Nguyễn_Minh_Trường.docx)
- [Slide PDF tóm tắt – 14 slide, khổ 16:9](deliverables/tieng_viet/slides/DDM501_Assignment1_25MS13312_Nguyen_Minh_Truong_Slides.pdf)
- [Ảnh tổng quan slide](deliverables/tieng_viet/slides/slide_preview.png)
- [Đề bài gốc](<INDIVIDUAL ASSIGNMENT 1_baiCaNhan.pdf>)

## Nội dung

Báo cáo thiết kế một hệ thống dự báo nhu cầu hằng ngày cho chuỗi bán lẻ giả định: 20 cửa hàng, khoảng 2.000 sản phẩm/cửa hàng, dự báo bảy ngày. Một mô hình dùng chung tạo dự báo; quy tắc tồn kho tạo đơn nháp và nhân viên phê duyệt trước khi gửi ERP.

Nội dung bám năm phần của rubric:

1. Định nghĩa bài toán, bối cảnh và các bên liên quan (20%).
2. Yêu cầu chức năng, phi chức năng và dữ liệu (20%).
3. Mục tiêu kinh doanh/hệ thống/mô hình và phương pháp kiểm chứng (20%).
4. Kiến trúc, quy trình ML, giám sát và khôi phục (25%).
5. Các đánh đổi thiết kế (15%).

Bản 2.1 có cơ sở học thuật, giả thuyết, so sánh mô hình, kiểm soát thời điểm dữ liệu/tồn kho, phân tích kinh tế và thử nghiệm theo cụm cửa hàng. Có bìa, mục lục PDF với liên kết, danh mục viết tắt và bảng/hình đánh số. Nội dung PDF dùng Times New Roman cỡ 12. Bản Word có trường mục lục; dùng **Update Field** nếu trình đọc chưa cập nhật số trang Word.

**Tình trạng bằng chứng:** đây là tài liệu thiết kế, chưa phải ứng dụng đã triển khai. Số liệu, ngân sách, đường cơ sở và mục tiêu đều là giả định được ghi rõ. Chưa có kết quả huấn luyện, kiểm thử tải hoặc thử nghiệm kinh doanh thực tế.

## Tổ chức mã nguồn

| Tệp | Mục đích |
| --- | --- |
| REPORT_VI.md | Nội dung nguồn của báo cáo tiếng Việt |
| student.json | Thông tin sinh viên dùng khi xuất tài liệu |
| build_report_vi.py | Tạo PDF, Word, sơ đồ và Markdown xuất bản |
| build_slides_vi.py | Tạo slide PDF và ảnh xem trước |
| verify_report.py | Kiểm tra bố cục, nội dung, thông tin sinh viên, trích dẫn và bookmark |
| build_report.py | Script bản tiếng Anh ban đầu |
| deliverables/tieng_viet/ | Báo cáo và tài liệu xuất mới nhất |
| requirements.txt | Phiên bản thư viện dùng tạo tài liệu |

Các bản lưu cũ, ảnh kiểm tra trung gian và bộ đệm chỉ lưu cục bộ, không đưa lên repository.

## Tạo lại tài liệu

Môi trường hiện tại: Windows, Python 3.14, các phông Arial và Times New Roman trong C:/Windows/Fonts. Các script sử dụng đường dẫn phông Windows; cần điều chỉnh nếu chạy trên hệ điều hành khác.

Với Python đã cài:

```powershell
python -m pip install -r requirements.txt
python build_report_vi.py
python verify_report.py --vietnamese
python build_slides_vi.py
```

Hoặc dùng uv:

```powershell
uv run --no-project --with-requirements requirements.txt python build_report_vi.py
uv run --no-project --with-requirements requirements.txt python verify_report.py --vietnamese
uv run --no-project --with-requirements requirements.txt python build_slides_vi.py
```

Trong workspace bị giới hạn quyền, thêm --cache-dir .uv-cache; khi thư viện đã có trong bộ đệm, có thể thêm --offline.

Sửa REPORT_VI.md để thay nội dung báo cáo rồi chạy lại script. Nội dung slide chỉnh trong build_slides_vi.py. Chỉnh Word trực tiếp không tự cập nhật PDF do script tạo; dùng Word xuất PDF nếu làm theo cách này.

## Kiểm tra chất lượng

File verification.json trong thư mục báo cáo và slide ghi kết quả kiểm tra xuất tài liệu. Các kiểm tra xác nhận chất lượng tài liệu, không chứng minh hiệu quả hệ thống ML đề xuất.
