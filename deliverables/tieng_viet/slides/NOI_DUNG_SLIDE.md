# Tóm tắt thuyết trình DDM501

BÀI TẬP CÁ NHÂN 1 • ML SYSTEM DESIGN

Dự báo nhu cầu hàng hóa
cho chuỗi bán lẻ

DDM501  •  25MS13312  •  Nguyễn Minh Trường

01 / 14


## 1. Dự báo nhu cầu hàng hóa
cho chuỗi bán lẻ

Một mô hình dùng chung.
Đề xuất bổ sung hàng có người phê duyệt.

Nguyễn Minh Trường  |  MSSV: 25MS13312
Học phần DDM501 – AI in DevOps, DataOps, MLOps

Tài liệu thiết kế: số liệu và mục tiêu là giả định; chưa có kết quả thực nghiệm.

Bản tóm tắt phục vụ thuyết trình • Báo cáo tiếng Việt phiên bản 2.1

01 • ĐỊNH NGHĨA BÀI TOÁN

Bài toán: giảm hết hàng và tồn kho dư

DDM501  •  25MS13312  •  Nguyễn Minh Trường

02 / 14


## 2. Bài toán: giảm hết hàng và tồn kho dư

BỐI CẢNH

20 cửa hàng
2.000 sản phẩm/cửa hàng
Giao hàng sau 1–3 ngày

HIỆN TRẠNG

Trung bình bán 28 ngày
Bảng tính và chỉnh tay
Thiếu đánh giá thống nhất

GIÁ TRỊ KỲ VỌNG

Giảm thiếu hàng
Giảm vốn tồn kho
Giảm thời gian lập đơn

Phạm vi: mặt hàng có lịch sử ổn định; sản phẩm mới hoặc quá gián đoạn dùng dự phòng.

01 • STAKEHOLDERS

Các bên liên quan và xung đột mục tiêu

DDM501  •  25MS13312  •  Nguyễn Minh Trường

03 / 14


## 3. Các bên liên quan và xung đột mục tiêu

CỬA HÀNG / LẬP KẾ HOẠCH

Có hàng để bán; hiểu đề xuất và được điều chỉnh.

KINH DOANH / TÀI CHÍNH

Giảm tồn kho; lợi ích phải bù chi phí.

DỮ LIỆU / ML

Nhãn đáng tin; so sánh công bằng; tái lập được.

VẬN HÀNH / MUA HÀNG / AN NINH

Kịp hạn; đơn khả thi; phân quyền và truy vết.

02 • YÊU CẦU CHỨC NĂNG VÀ PHI CHỨC NĂNG

Yêu cầu hệ thống: đủ chức năng, kịp thời hạn

DDM501  •  25MS13312  •  Nguyễn Minh Trường

04 / 14


## 4. Yêu cầu hệ thống: đủ chức năng, kịp thời hạn

CHỨC NĂNG

Dự báo 7 ngày theo cửa hàng–SKU
Tạo đơn nháp và duyệt trên giao diện
Tích hợp POS/ERP; lưu phiên bản
Chống đơn trùng; có dự phòng

NGƯỠNG ĐỀ XUẤT

40.000 cặp → 280.000 dòng/ngày
Công bố trước 05:30
Suy luận p95 ≤ 30 phút
API p95 ≤ 500 ms tại 20 yêu cầu/giây

Đúng hạn ≥ 99% ngày; API sẵn sàng ≥ 99,5%/tháng. Các ngưỡng cần kiểm thử tải.

02 • NGUỒN DỮ LIỆU VÀ QUYỀN RIÊNG TƯ

Dữ liệu: chất lượng quan trọng hơn số lượng

DDM501  •  25MS13312  •  Nguyễn Minh Trường

05 / 14


## 5. Dữ liệu: chất lượng quan trọng hơn số lượng

NGUỒN VÀ KHỐI LƯỢNG

POS, tồn kho, danh mục sản phẩm
Giá và khuyến mãi đã xác nhận
18 tháng ≈ 21,92 triệu dòng ngày
Lưu thời điểm dữ liệu có sẵn

KIỂM SOÁT

Không coi tệp thiếu là bán bằng 0
Loại nhãn ngày hết hàng khỏi ML
Không thu thập định danh khách hàng
Mã hóa, phân quyền, lưu có thời hạn

Lượng bán khi hết hàng không phản ánh đủ nhu cầu [6]; phải báo cáo thiên lệch và độ bao phủ.

03 • CƠ SỞ HỌC THUẬT VÀ LỰA CHỌN MÔ HÌNH

Vì sao chọn một LightGBM dùng chung?

DDM501  •  25MS13312  •  Nguyễn Minh Trường

06 / 14


## 6. Vì sao chọn một LightGBM dùng chung?

PHƯƠNG PHÁP CƠ SỞ

Trung bình 28 ngày
Cùng thứ trong 4 tuần
ETS theo chuỗi

Bắt buộc so sánh công bằng.

ỨNG VIÊN ML

Học tương tác lịch/giá
Chia sẻ dữ liệu giữa chuỗi
Đặc trưng + chân trời

Một mô hình cuối cùng.

GIỚI HẠN

M5 hỗ trợ chọn ứng viên [1]
Hiệu năng có thể đổi theo kỳ [2]

Không mặc định ML sẽ thắng.

Poisson dự báo kỳ vọng; WAPE là chỉ số nghiệm thu. Không giả định nhu cầu thật có phân bố Poisson.

04 • LUỒNG DỮ LIỆU VÀ KIỂM SOÁT

Kiến trúc: tách huấn luyện và vận hành

DDM501  •  25MS13312  •  Nguyễn Minh Trường

07 / 14


## 7. Kiến trúc: tách huấn luyện và vận hành

NGUỒN DỮ LIỆU

POS / ERP / Khuyến mãi

KIỂM TRA + ĐẶC TRƯNG

Ảnh chụp có phiên bản

HUẤN LUYỆN TUẦN

Đánh giá → duyệt → MLflow

SUY LUẬN THEO LÔ

Dự báo + quy tắc đặt hàng

CÔNG BỐ NGUYÊN TỬ

PostgreSQL → API

NHÂN VIÊN + ERP

Điều chỉnh → duyệt đơn

Giám sát dữ liệu, thực tế và đơn hàng → điều tra → ứng viên mới; phát hành luôn có người duyệt.

Phiên bản mô hình được cố định cho mỗi lần chạy; lưu dữ liệu/mã/chính sách để khôi phục [4].

04 • CHÍNH SÁCH BỔ SUNG HÀNG

Từ dự báo đến đơn hàng: đúng thời điểm

DDM501  •  25MS13312  •  Nguyễn Minh Trường

08 / 14


## 8. Từ dự báo đến đơn hàng: đúng thời điểm

Sáng ngày D: dữ liệu đến D−1 → dự báo D…D+6

Khoảng bảo vệ = thời gian giao L + chu kỳ xét đơn R
IP = hàng hiện có + hàng về đúng khoảng − giữ chỗ độc lập
S = tổng dự báo trong khoảng bảo vệ + tồn kho an toàn

Q = p × ceil(max(0, S − IP) / p)

Ví dụ giả định: L=2, R=1, S=70, IP=40, kiện p=6 → đặt 30 đơn vị.

Kiểm tra hàng về theo ETA; thiếu trước ngày giao cần ngoại lệ giao gấp/chuyển hàng.

03 • CÁC NGƯỠNG ĐỀ XUẤT, KHÔNG PHẢI KẾT QUẢ

Mục tiêu: từ kinh doanh đến mô hình

DDM501  •  25MS13312  •  Nguyễn Minh Trường

09 / 14


## 9. Mục tiêu: từ kinh doanh đến mô hình

HẾT HÀNG

8% →

≤ 6,4%

NGÀY TỒN KHO

12 ngày →

≤ 10,8 ngày

GIỜ/CỬA HÀNG/TUẦN

4 giờ →

≤ 2,5 giờ

Mô hình: WAPE ≤ 25% VÀ giảm tương đối ≥ 10% so với cơ sở tốt nhất.
Độ chệch tuyệt đối ≤ 5%; kiểm tra sai số từng nhóm và MASE.

Cơ sở là giả định cần đo lại. Chất lượng dự báo tốt chưa đủ chứng minh lợi ích kinh doanh.

03 • THIẾT KẾ KIỂM CHỨNG DỰ BÁO

Đánh giá ngoại tuyến: không rò rỉ tương lai

DDM501  •  25MS13312  •  Nguyễn Minh Trường

10 / 14


## 10. Đánh giá ngoại tuyến: không rò rỉ tương lai

THÁNG 1–12

Huấn luyện ban đầu

THÁNG 13–15

3 lượt xác thực tiến dần

THÁNG 16–18

Kiểm tra chưa dùng chọn

Giữ thứ tự thời gian; loại nhãn huấn luyện chồng cửa sổ tương lai.

Đặc trưng chỉ dùng thông tin đã biết tại thời điểm chốt.

So sánh cùng mẫu: WAPE, MAE/MASE, độ chệch và độ bao phủ.

Khung đánh giá dựa trên nghiên cứu về sai sót đánh giá dự báo [3] và xác thực chuỗi thời gian [5].

03 • PILOT VÀ ĐỘ TIN CẬY THỐNG KÊ

Thử nghiệm kinh doanh: cửa hàng là đơn vị mẫu

DDM501  •  25MS13312  •  Nguyễn Minh Trường

11 / 14


## 11. Thử nghiệm kinh doanh: cửa hàng là đơn vị mẫu

KẾ HOẠCH SƠ BỘ

2 tuần chạy quan sát
8 tuần thử nghiệm, 10 cặp cửa hàng
Ngẫu nhiên trong từng cặp
Phân tích theo nhóm phân ban đầu

ĐIỀU KIỆN KẾT LUẬN

Đo chênh lệch trước–sau theo cặp
Khoảng tin cậy 95%; kiểm tra độ bền
Giữ giới hạn tồn kho và hao hụt
Theo dõi ảnh hưởng giữa cửa hàng

10 cặp chưa chắc đủ phát hiện giảm 1,6 điểm phần trăm: cần tính cỡ mẫu trước khi chốt kế hoạch.

05 • TRADE-OFFS

Các đánh đổi: quyết định có điều kiện

DDM501  •  25MS13312  •  Nguyễn Minh Trường

12 / 14


## 12. Các đánh đổi: quyết định có điều kiện

Độ chính xác ↔ độ trễ

LightGBM trên CPU; giữ phương pháp cơ sở.

Độ mới ↔ chi phí

Theo lô hằng ngày; chỉ nâng tần suất khi có bằng chứng.

Đơn giản ↔ hiệu năng

Một mô hình chung; giám sát theo nhóm.

Tự động hóa ↔ kiểm soát

Đơn nháp có người duyệt và lưu lý do sửa.

Riêng tư ↔ độ chi tiết

Dữ liệu tổng hợp; không cần định danh khách hàng.

KẾT LUẬN • ĐIỀU KIỆN TRIỂN KHAI

Chỉ mở rộng khi bằng chứng và kinh tế cùng đạt

DDM501  •  25MS13312  •  Nguyễn Minh Trường

13 / 14


## 13. Chỉ mở rộng khi bằng chứng và kinh tế cùng đạt

KINH TẾ MINH HỌA

Hạ tầng: 500 USD/tháng
Hỗ trợ: 160 USD/tháng
Lợi ích giả định: 950 USD/tháng
Ròng: +290; giảm nửa lợi ích → −185

QUYẾT ĐỊNH

Dữ liệu đủ tốt, mô hình vượt cơ sở
Hệ thống đạt thời hạn và khôi phục
Pilot cải thiện, không phá giới hạn
Lợi ích ròng dương sau hỗ trợ

Chưa có dữ liệu thực hoặc kết quả huấn luyện. Nếu bằng chứng chưa đạt, tiếp tục dùng cơ sở.

TÀI LIỆU THAM KHẢO • SỐ THỨ TỰ RIÊNG CHO SLIDE

Nguồn chính và thông điệp cuối

DDM501  •  25MS13312  •  Nguyễn Minh Trường

14 / 14


## 14. Nguồn chính và thông điệp cuối

[1] Makridakis và cs. (2022). M5 accuracy competition.

[2] Ma & Fildes (2022). M5: A robustness check.

[3] Hewamalage và cs. (2023). Forecast evaluation: Common pitfalls.

[4] Sculley và cs. (2015). Hidden Technical Debt in ML Systems.

[5] Hyndman & Athanasopoulos (2021). Forecasting: Principles and Practice.

[6] Jain, Rudi & Wang (2015). Demand Estimation and Ordering Under Censoring.

Nguồn chi tiết và giả định: báo cáo tiếng Việt phiên bản 2.1.
Bấm vào tên tài liệu để mở nguồn.

Đóng góp của bài: thiết kế có thể kiểm chứng; hiệu quả thực tế phải được xác nhận trước mở rộng.