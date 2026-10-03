# Tài liệu thiết kế hệ thống học máy

## Dự báo nhu cầu hàng hóa hằng ngày cho chuỗi bán lẻ

Học phần: DDM501 – AI in DevOps, DataOps, MLOps.

Bài tập: Individual Assignment 1. Hình thức nộp: báo cáo viết. Tỷ trọng bài tập trong học phần: 5%.

Mã số sinh viên: {{student_id}}. Họ và tên: {{name}}.

Ngày lập báo cáo: 03/10/2026.

Phiên bản 2.1: thiết kế có cơ sở học thuật, phân tích độ nhạy, kế hoạch kiểm chứng và trình bày báo cáo học thuật.

## Tóm tắt

Báo cáo đề xuất thiết kế một hệ thống học máy (Machine Learning – ML) phục vụ chuỗi bán lẻ thực phẩm giả định tại Việt Nam, gồm 20 cửa hàng và khoảng 2.000 sản phẩm đang kinh doanh tại mỗi cửa hàng. Một mô hình dự báo dùng chung tạo dự báo nhu cầu theo ngày cho bảy ngày tiếp theo. Quy tắc bổ sung hàng chuyển dự báo thành số lượng đặt hàng đề xuất; nhân viên lập kế hoạch giữ quyền phê duyệt. Thiết kế bao quát chất lượng dữ liệu, thời hạn cung cấp kết quả, đánh giá theo thời gian, giám sát, khôi phục phiên bản và tác động kinh doanh có thể đo lường.

## Giả định và tình trạng bằng chứng

Doanh nghiệp, số liệu hiện trạng, chi phí, quy mô dữ liệu và các ngưỡng nghiệm thu đều là giả định thiết kế, không phải số liệu quan sát tại một doanh nghiệp thực tế. Báo cáo chưa huấn luyện mô hình và không khẳng định đã đạt được mức cải thiện nào. Cần đo đường cơ sở trong giai đoạn khảo sát và xác nhận mục tiêu qua thử nghiệm có nhóm đối chứng. Tài liệu kỹ thuật chính thức chỉ được dùng để xác nhận khả năng của công cụ.

## Cấu trúc theo tiêu chí chấm điểm

| Phần bắt buộc | Tỷ trọng | Vị trí |
| --- | --- | --- |
| Định nghĩa bài toán | 20% | Phần 1 |
| Phân tích yêu cầu | 20% | Phần 2 |
| Mục tiêu và chỉ số đánh giá | 20% | Phần 3 |
| Thiết kế kiến trúc tổng thể | 25% | Phần 4 |
| Phân tích các đánh đổi | 15% | Phần 5 |

## Câu hỏi thiết kế và cách tiếp cận

Câu hỏi trung tâm: một mô hình dự báo dùng chung có cải thiện quyết định bổ sung hàng so với chính sách hiện tại, trong giới hạn dữ liệu, chi phí và vận hành của doanh nghiệp hay không? Báo cáo áp dụng cách tiếp cận thiết kế dựa trên bằng chứng: tổng hợp nghiên cứu, xác lập yêu cầu, so sánh phương án, mô tả cơ chế triển khai và đề xuất phép kiểm chứng. Đóng góp của tài liệu là một thiết kế nhất quán và có thể kiểm tra; không tuyên bố đóng góp thuật toán mới hoặc kết quả thực nghiệm chưa có.

---

# 1. Định nghĩa bài toán (20%)

## 1.1 Bối cảnh và lý do lựa chọn

Giả định một doanh nghiệp bán lẻ khu vực vận hành 20 cửa hàng thực phẩm. Mỗi cửa hàng kinh doanh khoảng 2.000 mặt hàng thực phẩm đóng gói, đồ uống và đồ gia dụng. Nhà cung cấp giao hàng hằng ngày hoặc cách vài ngày; thời gian từ đặt hàng đến nhận hàng là một đến ba ngày. Nhu cầu thay đổi theo cửa hàng, ngày trong tuần, chương trình khuyến mãi và ngày lễ. Hiện nay, quản lý cửa hàng dùng bảng tính và báo cáo tồn kho từ hệ thống hoạch định nguồn lực doanh nghiệp (ERP) để ước lượng đơn hàng. Đặt thiếu gây hết hàng và mất cơ hội bán; đặt dư chiếm dụng vốn và tăng hao hụt đối với hàng có hạn sử dụng ngắn.

Phạm vi là dự báo hằng ngày theo cặp cửa hàng–sản phẩm cho các sản phẩm đã có lịch sử. Thử nghiệm ban đầu loại khỏi mô hình những sản phẩm có dưới 56 ngày lịch sử, nhu cầu quá gián đoạn hoặc cần tối ưu hạn sử dụng chuyên biệt. Các sản phẩm này được xử lý bằng quy tắc dự phòng và có nhãn trạng thái rõ ràng. Hệ thống không mở rộng sang tối ưu giá, gợi ý sản phẩm hoặc nhiều mô hình dự báo tương tác.

## 1.2 Phát biểu bài toán có thể đo lường

Mục tiêu là giảm tình trạng hết hàng có thể tránh được và tồn kho dư bằng cách cung cấp dự báo bảy ngày trước thời điểm chốt đơn hằng ngày. Giả định đường cơ sở của nhóm sản phẩm đủ điều kiện gồm: tỷ lệ hết hàng 8% trên số ngày cửa hàng–sản phẩm có mở bán; tồn kho tương đương 12 ngày cung ứng; nhân viên dành bốn giờ lập kế hoạch tại mỗi cửa hàng mỗi tuần.

Thử nghiệm đặt mục tiêu tỷ lệ hết hàng không quá 6,4% (giảm tương đối 20%), tồn kho giảm ít nhất 10% khi duy trì mức độ đáp ứng nhu cầu tương đương, và thời gian lập kế hoạch không quá 2,5 giờ/cửa hàng/tuần. Các kết quả này phải được đo trực tiếp; không suy ra chỉ từ độ chính xác dự báo.

## 1.3 Cách xử lý hiện tại

Nhân viên lấy lượng bán trung bình 28 ngày, điều chỉnh khuyến mãi bằng kinh nghiệm và nhân với thời gian giao hàng. Bảng tính riêng lưu tồn kho an toàn và quy cách đóng gói. Doanh nghiệp chưa có quy trình đánh giá thống nhất, lịch sử phiên bản mô hình hoặc phản hồi có hệ thống từ các điều chỉnh thủ công. Hiểu biết tại cửa hàng giúp nhận ra sự kiện bất thường, nhưng bảng tính không đồng nhất làm giảm khả năng kiểm tra và truy vết.

Chính sách hiện tại được dùng cho nhóm đối chứng kinh doanh. Trung bình lượng bán của cùng thứ trong bốn tuần trước cũng được đánh giá như một phương pháp dự báo cơ sở mạnh hơn.

## 1.4 Vì sao học máy phù hợp

Lịch sử bán hàng lặp lại cung cấp mẫu cho học có giám sát. Mô hình hồi quy dựa trên cây dùng chung có thể học quan hệ phi tuyến giữa lượng bán quá khứ, giá dự kiến, lịch, thuộc tính sản phẩm và cửa hàng; đồng thời tận dụng thông tin giữa các chuỗi dữ liệu. Điều này hữu ích khi một giá trị trung bình không thể biểu diễn mức tăng nhu cầu do khuyến mãi và khác biệt theo thứ trong tuần.

Việc dùng ML phụ thuộc vào bằng chứng: nếu mô hình không vượt qua phương pháp cơ sở đã được điều chỉnh hợp lý hoặc không đem lại lợi ích kinh doanh trong thử nghiệm, doanh nghiệp tiếp tục dùng chính sách đơn giản hơn.

Nghiên cứu M5 cho thấy cách dự báo dùng chung, đặc biệt các phương pháp dựa trên LightGBM, có tiềm năng trong bán lẻ nhiều chuỗi [4]. Đây là căn cứ chọn ứng viên, không phải bằng chứng mô hình đơn sẽ tái tạo kết quả thi. Ma và Fildes phát hiện hiệu năng các phương án đứng đầu thiếu ổn định qua các kỳ kiểm tra [5]. Vì vậy, cần nhiều cửa sổ thời gian trước khi kết luận mô hình tốt hơn.

Dự báo hướng đến nhu cầu khi có đủ hàng để bán. Khi hết hàng, lượng bán quan sát không phản ánh đầy đủ nhu cầu thực tế. Nếu coi mọi lượng bán ghi nhận là nhu cầu thật, mô hình có thể tiếp tục đề xuất đặt thiếu. Phần 2 trình bày cách loại trừ dữ liệu và bảo vệ quá trình đánh giá trước hạn chế này.

---

# 1.5 Các bên liên quan và ranh giới phạm vi

| Bên liên quan | Mục tiêu và mối quan tâm | Đáp ứng trong thiết kế |
| --- | --- | --- |
| Nhân viên lập kế hoạch, quản lý cửa hàng | Tránh hết hàng; hiểu đề xuất; giữ quyền xử lý tình huống tại cửa hàng. | Giao diện hiển thị lý do, phiên bản dự báo, trạng thái dự phòng; cho phép điều chỉnh và phê duyệt. |
| Bộ phận kinh doanh, tài chính | Nâng khả năng đáp ứng khách hàng nhưng không tăng tồn kho và chi phí vận hành. | Chỉ số kinh doanh trong thử nghiệm, giới hạn bảo vệ tồn kho và trần chi phí hằng tháng. |
| Nhà khoa học dữ liệu, kỹ sư ML | Nhãn đáng tin cậy; so sánh công bằng; phát hành có thể tái lập. | Đánh giá theo thời gian, phiên bản dữ liệu, chỉ số theo nhóm và điều kiện duyệt mô hình. |
| Kỹ sư dữ liệu, đội vận hành | Kịp thời hạn đặt hàng; phục hồi tác vụ lỗi; duy trì hợp đồng dữ liệu nguồn. | Kiểm tra hằng ngày, thử lại và lưu tiến độ, công bố trọn bộ kết quả, quy trình khôi phục. |
| Bộ phận an toàn thông tin, quản trị dữ liệu | Hạn chế quyền truy cập, lộ lọt và thời gian lưu dữ liệu. | Không thu thập định danh khách hàng; phân quyền dịch vụ; mã hóa và ghi nhật ký truy cập. |
| Bộ phận mua hàng, nhà cung cấp | Đơn hàng ổn định, khả thi theo thời gian giao và quy cách đóng gói. | Tích hợp ERP, ràng buộc năng lực cung ứng và xử lý ngoại lệ có người duyệt. |

## 1.6 Xung đột mục tiêu và cách giải quyết

Quản lý cửa hàng muốn tăng tồn kho an toàn, trong khi tài chính muốn giảm vốn lưu động. Hệ thống đặt giới hạn bảo vệ tỷ lệ hết hàng và chỉ công nhận giảm tồn kho khi vẫn duy trì khả năng có hàng để bán. Nhân viên muốn điều chỉnh theo kinh nghiệm, còn nhóm ML cần đánh giá nhất quán. Vì vậy, dự báo gốc và đơn hàng sau điều chỉnh đều được lưu để đánh giá riêng chất lượng dự báo và chất lượng quyết định.

## 1.7 Phạm vi và môi trường triển khai

Phiên bản khả dụng tối thiểu (MVP) phục vụ 40.000 cặp cửa hàng–sản phẩm, tạo 280.000 dòng dự báo cho các chân trời dự báo mỗi ngày. Kiến trúc gồm một mô hình dùng chung, một quy trình xử lý theo lô có lịch chạy, API đọc dự báo và giao diện lập kế hoạch. Hệ thống có thể chạy trên đám mây được quản lý hoặc hạ tầng hiện có của doanh nghiệp, với kho đối tượng được mã hóa và cơ sở dữ liệu quan hệ.

Huấn luyện và suy luận dùng CPU; cấu hình tài nguyên cụ thể được xác định bằng kiểm thử tải. Thu thập dữ liệu theo luồng, dịch vụ kho đặc trưng riêng và Kubernetes chỉ được xem xét khi số liệu vận hành chứng minh nhu cầu.

## 1.8 Các giả định cần xác nhận

Thiết kế giả định có tệp bán hàng hằng ngày từ hệ thống điểm bán (POS), ảnh chụp tồn kho, kế hoạch khuyến mãi đã xác nhận, mã sản phẩm ổn định và người phụ trách tích hợp ERP. Giai đoạn khảo sát cần xác nhận lịch mở cửa, độ chính xác tồn kho, khả năng có nhãn, thời gian giao hàng và các cửa hàng có thể so sánh trong thử nghiệm.

Đơn vị tài trợ cần xác nhận lợi ích đủ bù chi phí vận hành. Nếu thông tin hết hàng không đáng tin cậy, phải sửa quy trình đo lường trước khi kết luận hệ thống đã cải thiện nhu cầu dự báo hoặc tỷ lệ hết hàng.

---

# 1.9 Cơ sở học thuật và giả thuyết thiết kế

## Tổng hợp bằng chứng và giới hạn áp dụng

| Nguồn nghiên cứu | Ý nghĩa đối với thiết kế | Giới hạn áp dụng |
| --- | --- | --- |
| Makridakis và cộng sự (2022), M5 [4] | Động cơ thử mô hình chung có đặc trưng ngoại sinh. | Dữ liệu, chân trời và cách kết hợp mô hình khác bài toán này; không chuyển nguyên mức cải thiện. |
| Ma và Fildes (2022) [5] | Yêu cầu kiểm tra độ bền qua các kỳ. | Không thay được kiểm chứng trên chuỗi bán lẻ giả định. |
| Hewamalage và cộng sự (2023) [6] | Đánh giá phải phù hợp thời gian và đặc điểm dữ liệu. | Quy trình chia tập cụ thể cần thiết kế theo thời điểm có dữ liệu. |
| Jain, Rudi và Wang (2015) [7] | Khi hết hàng, lượng bán không biểu diễn đầy đủ nhu cầu. | Phương pháp suy luận trong nghiên cứu không được triển khai ở MVP. |
| Sculley và cộng sự (2015) [8] | Cần quản lý phụ thuộc dữ liệu và vòng phản hồi của hệ thống ML. | Không cung cấp sẵn cấu hình hoặc ngưỡng vận hành cho doanh nghiệp. |

Hewamalage và cộng sự nhấn mạnh rủi ro kết luận sai khi phân chia dữ liệu hoặc chọn thước đo không phù hợp chuỗi thời gian [6]. Báo cáo chuyển nguyên tắc đó thành quy tắc chốt dữ liệu, loại nhãn chồng lấn và đánh giá theo chân trời. Jain và cộng sự nghiên cứu ước lượng nhu cầu dưới kiểm duyệt do hết hàng, với thông tin thời điểm hết hàng [7]. MVP chỉ dùng cờ sẵn có để loại nhãn; nếu chưa thu được thời điểm hết hàng đáng tin cậy thì không thể tự khẳng định đã khôi phục nhu cầu tiềm ẩn.

## Giả thuyết có thể bác bỏ

H1 – Chất lượng dự báo: mô hình chung giảm WAPE tương đối ít nhất 10% so với cơ sở tốt nhất trên dữ liệu kiểm tra chưa dùng chọn mô hình, đồng thời giữ giới hạn độ chệch và chất lượng từng nhóm. Nếu không đạt, H1 chưa được ủng hộ và phương pháp cơ sở tiếp tục được sử dụng.

H2 – Tác động quyết định: gói can thiệp gồm dự báo ML, quy tắc đặt hàng và giao diện duyệt giảm hết hàng mà không làm tăng tồn kho/hao hụt vượt giới hạn. Thử nghiệm đo hiệu quả của cả gói, không quy toàn bộ thay đổi cho thuật toán riêng lẻ.

H3 – Khả thi vận hành: hệ thống hoàn thành trước giờ chốt ở tải thiết kế và có lợi ích ròng dương sau khi tính cả hỗ trợ. Không đạt thời hạn hoặc không hòa vốn là lý do dừng mở rộng ngay cả khi H1 đúng.

## Tính hợp lệ và giới hạn suy rộng

Tính hợp lệ nội tại bị đe dọa bởi hết hàng che khuất nhãn, tồn kho sai, can thiệp thủ công và phân bổ hàng giữa nhóm thử nghiệm. Tính hợp lệ đo lường bị đe dọa nếu các cửa hàng ghi nhận hết hàng khác nhau. Tính hợp lệ ngoại tại giới hạn ở mặt hàng ổn định trong chuỗi giả định; không suy rộng ngay sang sản phẩm mới, hàng cực kỳ gián đoạn hoặc chuỗi có năng lực cung ứng khác. Tính hợp lệ kết luận thống kê phụ thuộc số cửa hàng và tương quan theo thời gian, không phụ thuộc đơn thuần vào số triệu dòng SKU.

---

# 2. Phân tích yêu cầu (20%)

## 2.1 Yêu cầu chức năng và điều kiện nghiệm thu

| Mã | Yêu cầu | Điều kiện nghiệm thu |
| --- | --- | --- |
| FR-01 | Dự báo nhu cầu không âm cho ngày 1–7 của từng cặp cửa hàng–sản phẩm đang hoạt động, đủ điều kiện. | Có bảy kết quả với ngày đích duy nhất; cặp bị loại có bảy dòng dự phòng được đánh dấu. |
| FR-02 | Tạo lượng bổ sung đề xuất từ vị thế tồn kho, thời gian giao, tồn kho an toàn và quy cách đóng gói. | Lượng đặt không âm, đúng quy cách; có lý do cho ràng buộc hoặc ngoại lệ. |
| FR-03 | Tích hợp dữ liệu POS, tồn kho, sản phẩm, khuyến mãi; xuất bản nháp đã duyệt sang ERP. | Đối soát tổng nguồn; cách ly dữ liệu sai cấu trúc; khóa chống trùng ngăn tạo hai bản nháp ERP. |
| FR-04 | Cho phép tìm kiếm, lọc, xem dự báo, điều chỉnh và phê duyệt. | Nhân viên xem được sản phẩm, sửa đề xuất kèm lý do và gửi bản nháp có phiên bản. |
| FR-05 | Lưu nguồn gốc dữ liệu và phản hồi. | Mỗi dòng liên kết ảnh chụp nguồn, phiên bản đặc trưng/mã/mô hình, cờ dự phòng và ngày gốc dự báo; mỗi lần duyệt lưu người và thời điểm. |
| FR-06 | Khôi phục an toàn khi dữ liệu cũ, mô hình lỗi hoặc tính toán dở dang. | Không công bố một phần kết quả; cặp bị ảnh hưởng dùng dự phòng có nhãn; thử lại tích hợp không tạo trùng. |

## 2.2 Đặc tả đầu vào

Dữ liệu bán hàng hằng ngày gồm store_id, sku_id, local_business_date, units_sold, returns_units, unit_price và load_timestamp. Dữ liệu tồn kho gồm closing_on_hand, confirmed_inbound, reserved_units, stockout_flag và mức sẵn có quan sát được. Danh mục sản phẩm gồm category, pack_size, shelf_life_group và ngày bắt đầu/kết thúc kinh doanh. Danh mục cửa hàng gồm khu vực và lịch mở cửa.

Kế hoạch khuyến mãi đã xác nhận gồm ngày hiệu lực, giá dự kiến và loại khuyến mãi. ERP cung cấp thời gian giao của nhà cung cấp và giới hạn lượng đặt. Lượng bán là số đơn vị bán gộp không âm; hàng trả lại lưu riêng, không chuyển thành nhãn nhu cầu âm. Tên trường kỹ thuật được giữ nguyên để đặc tả tích hợp nhất quán.

## 2.3 Đặc tả đầu ra và quy tắc bổ sung hàng

Mỗi dòng dự báo gồm store_id, sku_id, forecast_origin, target_date, horizon_days, predicted_units, model_version, run_id, data_cutoff và quality_status. Đề xuất đặt hàng bổ sung inventory_position, lead_time_days, safety_stock_units, recommended_order_units, pack_size, exception_reason và approval_status.

Quy ước ngày gốc o là ngày bán hàng hoàn chỉnh cuối cùng đã quan sát. Lần chạy sáng ngày D chốt dữ liệu trước 01:00, dùng lịch sử đến D−1, nên o = D−1; chân trời h = 1 là D và h = 7 là D+6. Ví dụ: lần chạy sáng 2026-10-03 có forecast_origin = 2026-10-02, target_date = 2026-10-03, horizon_days = 1 và predicted_units = 18,6. Đây là minh họa cấu trúc, không phải kết quả huấn luyện. Quy ước bao gồm nhu cầu ngày xét đơn, tránh bỏ sót một ngày trong thời gian chờ hàng.

Đơn giản hóa thời gian: cửa hàng mở lúc 08:00; duyệt trước 06:00; đơn có thời gian giao L ngày đến trước khi mở cửa ngày D+L. Chu kỳ xét đơn R = 1 ngày. Khoảng bảo vệ gồm các ngày D đến D+L+R−1, dài L+R ngày và tối đa bốn ngày. Nếu thời gian giao nằm giữa ngày, cần dùng mô tả thời gian chi tiết hoặc chuyển ngoại lệ thủ công; không áp dụng máy móc giả định ngày tròn.

IP = hàng hiện có tại lúc duyệt + hàng đang về đã xác nhận trong khoảng bảo vệ − hàng giữ chỗ chưa nằm trong dự báo nhu cầu. S = tổng dự báo các ngày trong khoảng bảo vệ + SS. Q = p × ceil(max(0, S−IP)/p), trong đó SS là tồn kho an toàn, p là số đơn vị mỗi kiện. Không trừ hai lần hàng giữ chỗ nếu đó đã là một phần nhu cầu được dự báo. Hàng về sau khoảng bảo vệ không được tính để làm giảm đơn hiện tại.

Tồn kho an toàn ban đầu áp dụng quy tắc hiện có được nhân viên phê duyệt. Hạn sử dụng, sức chứa và giới hạn nhà cung cấp có thể giảm lượng đặt; xung đột phải hiện thành ngoại lệ. Dự báo giữ dạng số thập phân; đơn hàng làm tròn theo đơn vị và quy cách. Đơn ERP cần nhân viên phê duyệt.

Ví dụ giả định: L = 2, R = 1; dự báo D/D+1/D+2 là 18/20/22; SS = 10; hàng hiện có 30; hàng đang về ngày D+1 là 12; hàng giữ chỗ độc lập 2; p = 6. Khi đó S = 70, IP = 40 và Q = 30 đơn vị. Kiểm tra thêm tồn kho dự kiến theo từng ngày: tồn đầu ngày cộng hàng về đúng ngày trừ nhu cầu dự kiến. Nếu thiếu trước D+L, đơn mới không thể sửa thiếu hụt trước khi đến; cảnh báo để chuyển hàng/giao gấp thay vì coi Q là đã giải quyết hết hàng. Ví dụ này minh họa logic, không chứng minh hiệu quả tồn kho.

---

# 2.4 Yêu cầu phi chức năng và dữ liệu

| Khía cạnh | Yêu cầu đề xuất | Kiểm chứng và xử lý |
| --- | --- | --- |
| Hiệu năng | Công bố trước 05:30, múi giờ Asia/Bangkok; suy luận theo lô p95 ≤ 30 phút tại tải MVP; API đọc dữ liệu lưu sẵn p95 ≤ 500 ms ở 20 yêu cầu/giây. | Đo thời gian tác vụ và API trong kiểm thử tải đại diện; phân biệt độ trễ API với thời gian suy luận mô hình. |
| Khả năng mở rộng | 40.000 cặp, 280.000 dòng/ngày; thiết kế cho tải gấp ba: 120.000 cặp, 840.000 dòng, suy luận trong 60 phút. | Chia tác vụ theo cửa hàng; dùng ảnh chụp đặc trưng cố định và số tiến trình CPU song song có giới hạn. |
| Độ tin cậy | Ít nhất 99% ngày công bố đầy đủ, đúng hạn trong cửa sổ 90 ngày; API sẵn sàng ít nhất 99,5% mỗi tháng. | Lưu tiến độ, đổi con trỏ lần chạy hiện hành nguyên tử, hai bản sao API; kết quả dự phòng vẫn giữ trạng thái chất lượng. |
| Khôi phục | RTO ≤ 60 phút từ lúc phát hiện sự cố; RPO ≤ 24 giờ đối với dữ liệu nguồn đã lưu bền vững. | Sao lưu hằng ngày, xử lý lại tệp nguồn bất biến; diễn tập khôi phục mỗi quý; trễ nguồn chuyển sang dự phòng. |
| Bảo trì | Tạo ứng viên huấn luyện lại hằng tuần; kiểm tra dữ liệu và tác vụ hằng ngày; rà soát dự báo đã có kết quả thực tế hằng tuần. | Quản lý phiên bản cấu trúc/đặc trưng/cấu hình; điều tra khi dữ liệu thay đổi; phát hành phải vượt kiểm tra và được duyệt. |
| An toàn thông tin | Quyền tối thiểu theo vai trò; mã hóa truyền và lưu; ghi nhật ký phê duyệt. | Tách vai trò thu thập/huấn luyện/lập kế hoạch; dùng kho bí mật; rà soát trước triển khai. |

## 2.5 Nguồn, chất lượng, khối lượng và quyền riêng tư

Giả định có 18 tháng lịch sử, khoảng 548 ngày: 20 × 2.000 × 548 = 21,92 triệu dòng cửa hàng–sản phẩm–ngày. Tệp nguồn hằng ngày đến trước 01:00. Dự trù khoảng 100 GB cho các lần sửa dữ liệu thô, ảnh chụp đã xử lý, tệp mô hình và phần phụ trợ; cần đo dung lượng nén thực tế khi khảo sát. Mở rộng mẫu cho bảy chân trời có thể đạt khoảng 153 triệu dòng, nên lấy mẫu ngày gốc theo cách có thể tái lập hoặc xử lý từng phân vùng thay vì nạp toàn bộ vào bộ nhớ.

Áp dụng tính duy nhất của store_id/sku_id/date, khóa ngoại hợp lệ, lượng bán gộp không âm và khoảng hợp lý cho tồn kho/giá. Phân biệt tệp thiếu với ngày mở bán thực sự không bán được hàng. Đối soát tổng lượng bán từng cửa hàng với POS với sai lệch không quá 0,1%; phải có ít nhất 99% khóa đủ điều kiện dự kiến, và ít nhất 99,5% dòng nhận được vượt kiểm tra cấu trúc/miền giá trị. Loại trùng theo phiên bản nguồn và cách ly dòng không hợp lệ. Cửa hàng lỗi nhận kết quả dự phòng; không tự điền lượng bán bằng không. Thiếu tồn kho quan trọng thì chặn xuất đơn.

Thu thập cờ sẵn có để nhận diện nhãn bị giới hạn bởi hết hàng. Loại ngày đích đã biết hết hàng khỏi huấn luyện chính và chỉ số sai số trên lượng bán quan sát; loại lịch sử bị thiếu hàng nghiêm trọng khỏi phạm vi ML. Đặc trưng trễ có cờ sẵn có/thiếu dữ liệu để thể hiện lượng bán bị hạn chế. Cách này giảm nhưng không loại bỏ thiên lệch chọn mẫu: phải báo cáo độ bao phủ thông tin sẵn có và xác nhận tác động hết hàng trong thử nghiệm tương lai. Sai số trên lượng bán quan sát không trực tiếp đo nhu cầu bị mất chưa quan sát được.

Không thu thập tên khách hàng, mã khách hàng thân thiết hoặc định danh ở cấp giỏ hàng. Dữ liệu tổng hợp hằng ngày là đủ. Định danh nhân viên chỉ có trong nhật ký phê duyệt bị hạn chế truy cập. Thời hạn lưu đề xuất: dữ liệu bán thô/đã xử lý 24 tháng, dự báo/phê duyệt 12 tháng, nhật ký vận hành 90 ngày; cần phù hợp chính sách tổ chức. Hạn chế quyền tải xuống, mã hóa, ghi nhật ký truy cập và xóa phân vùng/bản sao lưu hết hạn theo chính sách được duyệt; báo cáo không mặc định đã đáp ứng mọi yêu cầu pháp lý.

---

# 2.6 Hợp đồng dữ liệu và tính khả thi của phạm vi

## Ngữ nghĩa thời gian và nhãn

Mỗi bản ghi phân biệt ngày nghiệp vụ (event_date), thời điểm nguồn công bố (available_at) và thời điểm nhận (ingested_at). Tại thời điểm chốt C, chỉ dùng bản ghi available_at ≤ C; sửa nguồn sau C không được hồi tố vào đặc trưng của lần đánh giá đó. Danh mục, giá và khuyến mãi phải có lịch sử phiên bản hiệu lực. Nếu chỉ có danh mục mới nhất, cần công bố giới hạn và loại đặc trưng không tái tạo được theo thời điểm lịch sử.

Nhãn y(s,k,o,h) là lượng bán gộp tại cửa hàng s, sản phẩm k, ngày o+h khi mở bán và có đủ hàng. Đây là đại diện có điều kiện của nhu cầu, không phải nhu cầu tiềm ẩn đầy đủ. Ngày đóng cửa có nhu cầu bán tại cửa hàng bằng không theo lịch; ngày thiếu tệp không được gán nhãn không. Kiểm tra tổng nhãn Poisson dương trước huấn luyện; các nhóm toàn số không chuyển dự phòng.

## Tiêu chí đủ điều kiện có thể triển khai

Quy tắc ban đầu đề xuất: ít nhất 56 ngày lịch sử; ít nhất 95% ngày mở cửa trong 56 ngày có dữ liệu hợp lệ; không quá 20% ngày hết hàng hoặc thiếu trạng thái sẵn có; lượng bán dương trên ít nhất 20% ngày mở cửa đủ dữ liệu. Đây là ngưỡng vận hành cần kiểm tra độ nhạy, không phải chuẩn chung. So sánh cửa sổ 56/84 ngày và giới hạn thiếu hàng 10%/20%/30% trên tập xác thực; cố định trước tập kiểm tra.

Độ bao phủ ML = số cặp đang hoạt động được dự báo bằng mô hình / tổng cặp đang hoạt động cần kết quả. Không loại cặp khó khỏi mẫu số để làm đẹp mục tiêu 95%. Nếu nhóm đủ điều kiện dưới 95%, phải ghi rõ mục tiêu chưa khả thi và duyệt lại phạm vi hoặc tăng năng lực xử lý dữ liệu trước nghiệm thu. Dự phòng có thể giúp công bố đủ bộ đúng hạn nhưng không được tính là ML.

## Cập nhật tồn kho và ràng buộc an toàn

Giữ forecast_origin khi nhân viên duyệt, nhưng làm mới IP từ ERP lúc duyệt để phản ánh bán phát sinh, hàng về và giữ chỗ. Ngưỡng đề xuất: ảnh chụp tồn kho không quá hai giờ tại lúc duyệt; quá ngưỡng thì chặn xuất hoặc dùng quy trình thủ công có lý do. Mỗi đề xuất lưu inventory_as_of, ETA của hàng đang về và phiên bản chính sách. Không huấn luyện lại chỉ vì tồn kho đổi.

Mô phỏng tồn kho theo ngày phát hiện thiếu trước lúc đơn mới đến và hàng hết hạn không thể bán. Chỉ trừ hàng đang về đúng khoảng liên quan. Giới hạn sức chứa/nhà cung cấp có thể làm mục tiêu dịch vụ không đạt; giao diện phải thể hiện thiếu hụt còn lại và người xử lý, thay vì chỉ đưa số đặt hàng có vẻ khả thi.

---

# 3. Mục tiêu và chỉ số đánh giá (20%)

## 3.1 Phân cấp mục tiêu và ngưỡng đề xuất

Mục tiêu kinh doanh là cải thiện hiệu quả bổ sung hàng. Mục tiêu hệ thống là giao đề xuất đáng tin cậy trước giờ đặt hàng. Mục tiêu mô hình là dự báo chính xác hơn quy tắc mùa vụ. Độ chính xác hỗ trợ quyết định nhưng lợi ích còn phụ thuộc vào tồn kho, thời gian giao và cách nhân viên sử dụng đề xuất. Các giá trị sau là ngưỡng đề xuất cho triển khai hoặc thử nghiệm; số liệu cơ sở là giả định cho đến khi được đo.

| Tầng và chỉ số | Đường cơ sở | Mục tiêu hoặc điều kiện quyết định |
| --- | --- | --- |
| Kinh doanh: tỷ lệ hết hàng | Giả định trung bình cửa hàng 8% trên ngày cửa hàng–sản phẩm đủ điều kiện, có mở bán. | Không quá 6,4% theo cùng cách tổng hợp trong thử nghiệm đối chứng; giảm tương đối 20%. |
| Kinh doanh: số ngày tồn kho đủ cung ứng (DOS) | Giả định 12 ngày. | Không quá 10,8 ngày, đồng thời duy trì giới hạn bảo vệ tỷ lệ hết hàng. |
| Kinh doanh: thời gian lập kế hoạch | Giả định 4 giờ/cửa hàng/tuần. | Không quá 2,5 giờ/cửa hàng/tuần, đo từ nhật ký thời gian. |
| Kinh doanh: chi phí và lợi ích | Chưa có chi phí ML; chưa đo hao hụt/lợi nhuận mất do hết hàng. | Chi phí hệ thống định kỳ đề xuất ≤ 500 USD/tháng; lợi nhuận gộp tăng thêm + hao hụt tránh được − chi phí vận hành tăng thêm > 0. |
| Hệ thống: thời hạn công bố | Chưa ghi nhận thống nhất thời gian giao thủ công. | Ít nhất 99% ngày có trọn bộ kết quả trước 05:30 trong 90 ngày; ít nhất 95% cặp dùng chế độ ML. |
| Hệ thống: API và xử lý lô | Chưa có phép đo triển khai tương đương. | API p95 ≤ 500 ms tại 20 yêu cầu/giây; suy luận MVP p95 ≤ 30 phút; API sẵn sàng ≥ 99,5%/tháng. |
| Mô hình: WAPE theo đơn vị, gộp ngày 1–7 | Giả định minh họa phương pháp mùa vụ đã điều chỉnh có WAPE 30%. | WAPE ≤ 25% VÀ cải thiện tương đối ≥ 10% so với phương pháp cơ sở tốt nhất được đo thực tế. |
| Mô hình: độ chệch và bảo vệ nhóm | Cần đo cho từng phương pháp cơ sở. | Độ chệch có dấu tuyệt đối ≤ 5%; WAPE của nhóm cửa hàng/danh mục quan trọng không xấu hơn cơ sở quá 2 điểm phần trăm. |

## 3.2 Định nghĩa chỉ số kinh doanh

Tỷ lệ hết hàng của mỗi cửa hàng = số ngày sản phẩm đủ điều kiện có ít nhất một lần hết hàng được xác nhận / tổng số ngày sản phẩm đủ điều kiện có mở bán tại cửa hàng đó. Chỉ số chính là trung bình các cửa hàng với trọng số bằng nhau; báo cáo thêm tỷ lệ gộp toàn bộ ngày cửa hàng–sản phẩm như chỉ số phụ. Cách quan sát tồn kho phải nhất quán giữa hai nhóm; không thay trọng số sau khi xem kết quả.

DOS = tồn kho bình quân theo đơn vị / lượng bán bình quân mỗi ngày trong cùng kỳ đánh giá, tính trong từng SKU rồi tổng hợp bằng trọng số giá trị tồn kho đã xác định trước. Loại SKU có lượng bán bằng không khỏi DOS và báo cáo riêng. Hết hàng có thể làm giảm mẫu số lượng bán, nên đọc DOS cùng tỷ lệ có hàng, giá trị tồn kho và hao hụt.

Thời gian lập kế hoạch bao gồm xem xét, điều chỉnh và gửi đề xuất bổ sung hàng, không chỉ thời gian trên giao diện. Đo các tuần đại diện ở cả hai nhóm. Lợi ích ròng dùng lợi nhuận gộp tăng thêm và hao hụt giảm so với đối chứng, trừ chi phí hạ tầng và hỗ trợ tăng thêm. Không tính tiền giải phóng từ tồn kho thành lợi nhuận định kỳ. Mục tiêu tiền tệ cần xác nhận khi tài chính cung cấp biên lợi nhuận và chi phí lưu kho.

---

# 3.3 Đánh giá mô hình và xác nhận kinh doanh

## Công thức và cách diễn giải

Với lượng bán thực tế quan sát y và dự báo f trên các ngày đích đủ điều kiện: WAPE = 100 × tổng(|y − f|) / tổng(y). Chỉ số có trọng số theo lượng bán toàn bộ các dòng, không phải trung bình sai số phần trăm của từng dòng. Nếu tổng lượng bán của một nhóm bằng không, WAPE không xác định; dùng MAE của nhóm đó.

Độ chệch có dấu = 100 × tổng(f − y) / tổng(y); giá trị dương thể hiện dự báo cao hơn thực tế. Báo cáo thêm MAE theo đơn vị, WAPE từng chân trời và từng nhóm cửa hàng/danh mục. Xác định trước nhóm quan trọng: chiếm ít nhất 1% lượng bán được đánh giá và có ít nhất 100 dòng đủ điều kiện.

WAPE dễ đọc theo tổng lượng bán nhưng có thể che sai số ở SKU lượng bán thấp. Bổ sung MASE mùa vụ theo chuỗi: MAE đánh giá / trung bình độ lệch tuyệt đối giữa y(t) và y(t−7) trong tập huấn luyện. Với mặt nạ sẵn có, chỉ tính mẫu số từ cặp ngày đều hợp lệ và công bố đây là MASE điều chỉnh mặt nạ. Mẫu số bằng không hoặc thiếu cặp thì báo cáo MAE và số chuỗi bị loại, không chia cho số nhỏ tùy tiện. Định nghĩa MASE tham khảo [9]; áp dụng mặt nạ là lựa chọn riêng của thiết kế.

Mỗi chỉ số phải kèm tỷ lệ bao phủ và số dòng loại vì hết hàng hoặc thiếu dữ liệu. Ứng viên và cơ sở dùng cùng dòng đích, thời điểm chốt đầu vào và quy tắc làm tròn. Hai cơ sở chỉ dùng dữ liệu đã có tại từng ngày gốc lịch sử: chính sách trung bình 28 ngày và trung bình của cùng thứ trong bốn tuần trước. Hệ số khuyến mãi đơn giản chỉ điều chỉnh trên tập huấn luyện; chọn cơ sở tốt nhất bằng tập xác thực.

## Xác thực theo thời gian và ngăn rò rỉ dữ liệu

Sử dụng lịch sử giả định 18 tháng: huấn luyện tháng 1–12, xác thực tháng 13; huấn luyện tháng 1–13, xác thực tháng 14; huấn luyện tháng 1–14, xác thực tháng 15. Sau các lượt tiến dần này, cố định định nghĩa đặc trưng, siêu tham số và phương pháp cơ sở. Huấn luyện lại bằng dữ liệu đến tháng 15 và đánh giá một lần trên tháng 16–18 chưa từng dùng để lựa chọn mô hình.

Chia tập theo ngày gốc dự báo cho toàn bộ cửa hàng cùng lúc. Mọi ngày gốc huấn luyện cộng cửa sổ nhãn bảy ngày phải kết thúc trước ngày gốc xác thực/kiểm tra đầu tiên; giới hạn đặc trưng theo thời điểm dữ liệu thực sự có sẵn. Cách này tránh nhãn tương lai chồng lấn và rò rỉ từ sửa hồi tố. Đánh giá tiến dần qua ngày gốc, nhiều chân trời tham khảo [10]. TimeSeriesSplit [2] hỗ trợ nguyên tắc thứ tự; áp dụng trực tiếp lên dòng SKU chưa gom theo ngày không bảo đảm phép chia đúng.

Dùng học có giám sát trực tiếp cho nhiều chân trời: một mô hình nhận đặc trưng tại ngày gốc, chân trời và lịch/khuyến mãi ngày đích đã biết trước. Với o = D−1, độ trễ 1/7/14/28 tại D dùng y(D−1), y(D−7), y(D−14), y(D−28); cửa sổ trượt kết thúc ở o. Không dùng lượng bán/giá thực tế tương lai hoặc kế hoạch sửa hồi tố. Giá dự kiến chỉ hợp lệ khi xác nhận trước chốt. Cờ hết hàng ngày đích dùng chọn nhãn, không trở thành đặc trưng biết trước tương lai.

Đánh giá chính tháng 16–18 dùng tệp mô hình đã cố định, nhưng cập nhật đặc trưng bằng lịch sử thật đã có ở từng ngày gốc. Có thể đánh giá phụ quy trình huấn luyện lại tuần bằng phát lại lịch sử, chỉ dùng nhãn đã đủ ngày tại lần huấn luyện đó; không điều chỉnh siêu tham số sau khi xem tập kiểm tra. Hai kết quả phải tách rõ, tránh nhầm độ chính xác mô hình cố định với hiệu quả chính sách bảo trì.

## Thiết kế thử nghiệm và quyết định phát hành

Chạy hai tuần ở chế độ quan sát: tạo dự báo nhưng không thay quyết định thực tế. Sau đó dự kiến thử nghiệm tám tuần với 10 cặp cửa hàng tương đồng, phân ngẫu nhiên trong từng cặp vào nhóm sử dụng ML hoặc đối chứng; ghép cặp theo quy mô và cơ cấu danh mục. Đây là kế hoạch sơ bộ, chỉ chốt sau phân tích cỡ mẫu ở mục 3.5. Nhóm sử dụng nhận đơn nháp ML, nhóm đối chứng giữ chính sách hiện tại. Ghi nhận điều chỉnh, khuyến mãi, lỗi nhà cung cấp và lượng bán bị giới hạn do hết hàng.

Sử dụng khoảng bất định có xét cụm cửa hàng; công bố trước chỉ số chính về hết hàng, giới hạn bảo vệ DOS và quy tắc loại trừ. Biến động lịch sử cùng mức tác động tối thiểu có ý nghĩa kinh doanh quyết định cỡ mẫu và sức mạnh thống kê trước khi chạy. Kéo dài thử nghiệm nếu 20 cửa hàng và tám tuần chưa đủ.

Triển khai rộng cần đạt mục tiêu điểm ước lượng về hết hàng và có khoảng bất định ủng hộ cải thiện, giữ giới hạn tồn kho/hao hụt, đạt thời gian thao tác chấp nhận được và lợi ích ròng ước tính dương. Nếu chưa rõ, thực hiện kế hoạch đo tiếp đã xác lập trước. Vượt kiểm tra ngoại tuyến chỉ cho phép chạy quan sát/thử nghiệm. Tài chính và vận hành duyệt mở rộng dựa trên kinh doanh; mục 3.5 quy định phép ước lượng và dừng.

---

# 3.4 Cơ sở ngưỡng mục tiêu và phân tích độ nhạy

## Phân biệt mục tiêu, giả định và bằng chứng

| Ngưỡng đề xuất | Cơ sở lập kế hoạch | Cách kiểm chứng trước quyết định |
| --- | --- | --- |
| Hết hàng 8% xuống 6,4% | 8% × (1−20%) = 6,4%; giảm tuyệt đối 1,6 điểm phần trăm; mục tiêu kinh doanh mong muốn. | Đo hiện trạng cùng định nghĩa; kiểm tra cỡ mẫu và đối chứng; không coi 20% là kết quả M5. |
| DOS 12 xuống 10,8 ngày | 12 × 0,9 = 10,8; giảm tương đối 10%. | Đo tồn kho thực tế, kèm hết hàng, giá trị tồn kho và hao hụt. |
| WAPE ≤ 25% và giảm ≥ 10% | Cơ sở 30% xuống 25% tương đương giảm 16,7%. Hai điều kiện cùng áp dụng. | Nếu cơ sở đo được 20%, ngưỡng thực tế ≤ 18%; ngưỡng = min(25%, 0,9 × WAPE cơ sở). |
| Suy luận 30 phút | Chừa khoảng phục hồi hai giờ từ mốc dự kiến 03:30 đến hạn 05:30. | Kiểm thử với CPU, dữ liệu và tiến trình xác định; đo cả tạo đặc trưng và xuất kết quả. |
| Hạ tầng ≤ 500 USD/tháng | Trần ngân sách đề xuất, chưa phải báo giá. | Đo tài nguyên, lấy báo giá; tính riêng hỗ trợ và xây dựng ban đầu. |

Không xem 25% WAPE, PSI 0,2 hoặc 500 USD là tiêu chuẩn phổ quát. Chủ nghiệp vụ phải xác nhận theo mức chịu rủi ro và giá trị kinh tế. SLO 99% ngày đúng hạn trong 90 ngày nghĩa là không được có ngày trễ: 89/90 chỉ đạt 98,89%. Báo cáo số ngày vi phạm và tỷ lệ chính xác; không làm tròn để coi một lần trễ là đạt.

## Kịch bản kinh tế minh họa, không phải báo giá

Phân bổ trần hạ tầng giả định 500 USD/tháng: xử lý lô 150, cơ sở dữ liệu 100, kho/sao lưu 70, API 80, giám sát/mạng/dự phòng 100. Hỗ trợ giả định 8 giờ × 20 USD = 160 USD/tháng; tổng định kỳ là 660 USD. Bảng này dùng kiểm tra hòa vốn, không chứng minh cấu hình hai bản sao đã mua được ở mức giá đó.

Kịch bản cơ sở giả định: lợi nhuận gộp tăng thêm 800 USD và hao hụt tránh được 150 USD/tháng; không quy đổi thời gian tiết kiệm thành tiền. Lợi ích ròng = 800+150−660 = 290 USD/tháng. Nếu lợi ích giảm một nửa, ròng = 400+75−660 = −185 USD/tháng. Nếu chi phí tăng 50%, ròng = 950−990 = −40 USD/tháng. Phải đo các đầu vào trước mở rộng vì kết quả nhạy với giả định.

Điểm hòa vốn lợi nhuận gộp tăng thêm là 660−150 = 510 USD/tháng nếu giảm hao hụt 150 USD được xác nhận. Chi phí xây dựng C0 tính riêng; thời gian hoàn vốn = C0 / lợi ích ròng tháng khi ròng dương. Không tính cùng phần hàng vừa là giảm hao hụt vừa là tăng lợi nhuận bán. Giờ công giảm chỉ quy tiền khi tài chính xác nhận giảm chi phí hoặc tái phân bổ có giá trị; nếu không, báo cáo riêng như lợi ích năng suất.

---

# 3.5 Đặc tả thử nghiệm và độ tin cậy kết luận

## Đơn vị phân bổ và tác động cần ước lượng

Đơn vị ngẫu nhiên là cửa hàng, không phải dòng SKU. Tạo 10 cặp từ 20 cửa hàng bằng đặc điểm trước can thiệp; trong mỗi cặp phân ngẫu nhiên một cửa hàng nhận hệ thống, một đối chứng, lưu hạt giống và danh sách phân bổ. Cố định SKU đánh giá từ thời kỳ trước; không loại ngày hết hàng sau can thiệp khỏi chỉ số kinh doanh. Phân tích theo nhóm được phân ban đầu (intention-to-treat), gồm cả cửa hàng dùng dự phòng hoặc ít dùng đề xuất.

CONSORT mở rộng cho thử nghiệm cụm yêu cầu minh bạch về đơn vị phân bổ, cỡ mẫu và tương quan trong cụm [11]. Báo cáo vận dụng nguyên tắc này cho cửa hàng; không phải thử nghiệm lâm sàng và không tuyên bố tuân thủ mọi quy định nghiên cứu y khoa.

Gọi r(i,t) là tỷ lệ ngày hết hàng của cửa hàng i trong kỳ t trên danh sách cố định. Chỉ số chính là trung bình cửa hàng với trọng số bằng nhau, nhất quán giữa cơ sở và mục tiêu 6,4%; tỷ lệ gộp theo SKU-ngày là chỉ số phụ. Ngày đóng cửa không thuộc mẫu số. Thiếu đo lường không tự coi là không hết hàng: báo cáo độ thiếu và phân tích biên khi coi toàn bộ ngày thiếu là có/không hết hàng.

## Phép ước lượng và khoảng tin cậy

Với cặp j, d(j) = [r(ML,sau)−r(ML,trước)] − [r(đối chứng,sau)−r(đối chứng,trước)]. Tác động tuyệt đối là trung bình 10 d(j); âm biểu thị giảm hết hàng. Ngẫu nhiên hóa hỗ trợ diễn giải nhân quả; hiệu chỉnh trước–sau tăng độ chính xác, không thay ngẫu nhiên hóa. Báo cáo thêm chênh lệch sau can thiệp chưa hiệu chỉnh để kiểm tra độ bền.

Khoảng tin cậy 95% theo cặp = trung bình d ± t(0,975;9) × SD(d)/sqrt(10), với t xấp xỉ 2,262. Giả định các cặp độc lập và chênh lệch không quá lệch. Với chỉ 10 cặp, bổ sung kiểm định ngẫu nhiên hóa từ 2^10 = 1.024 cách hoán đổi nhãn trong cặp dưới giả thuyết không tác động. Không coi triệu dòng SKU là mẫu độc lập hoặc dùng sai số chuẩn dòng đơn để tạo khoảng tin cậy quá hẹp.

## Cỡ mẫu, tương tác giữa nhóm và quy tắc dừng

Số cặp sơ bộ n ≈ [(1,96+0,84) × SD(d)/0,016]^2 cho mức ý nghĩa hai phía 5%, sức mạnh 80% và hiệu ứng 1,6 điểm phần trăm. Nếu SD(d) giả định 0,02, cần khoảng 13 cặp theo xấp xỉ chuẩn, vượt 10 cặp hiện có; với 0,03 cần khoảng 28 cặp. Đây là minh họa, không phải cỡ mẫu thực tế. Cần mô phỏng dữ liệu cụm/tuần trước thử nghiệm, hiệu chỉnh mẫu nhỏ và kiểm tra các thời lượng. Tăng số tuần không bảo đảm thay được thiếu cửa hàng.

Giữ quy tắc phân bổ kho chung; không ưu tiên hàng khan hiếm cho nhóm ML làm thiệt đối chứng. Ghi chuyển hàng và khả năng khách chuyển cửa hàng để xem xét hiệu ứng lan truyền. Nếu tương tác mạnh, cần phân bổ theo vùng cung ứng hoặc giới hạn kết luận; ngẫu nhiên theo cửa hàng có thể không còn phù hợp.

Đánh giá cuối kỳ tám tuần theo kế hoạch; không kéo dài chỉ vì p-value chưa đạt. Muốn tăng thời lượng phải quyết định trước khi xem kết quả phân nhóm. Theo dõi an toàn tuần: đề xuất dừng nếu hết hàng tăng trên 2 điểm phần trăm hoặc hao hụt theo giá vốn tăng trên 0,5 điểm phần trăm so với đối chứng trong hai tuần, hoặc có đơn trùng/sai tồn kho nghiêm trọng. Đây là ngưỡng quản trị, không phải kiểm định hiệu quả lặp lại.

Mở rộng khi nhóm sử dụng đạt mục tiêu, khoảng tin cậy tác động có cận trên dưới 0, DOS giảm theo mục tiêu, hao hụt không vượt giới hạn đã duyệt và lợi ích ròng dương. Khoảng tin cậy chỉ ủng hộ tác động khác không, không chứng minh chắc chắn giảm ít nhất 20%; muốn khẳng định mức tối thiểu đó phải thiết kế điều kiện và cỡ mẫu mạnh hơn.

Tỷ lệ hao hụt theo giá vốn = giá vốn hàng hủy/giảm giá trị do hết hạn hoặc hư hỏng trong kỳ / giá vốn hàng sẵn có đầu kỳ cộng nhập kho trong kỳ. Giữ cùng quy tắc định giá giữa nhóm và kỳ; khoản hàng chuyển giữa cửa hàng phải đối soát, không tính hai lần. Ngưỡng an toàn 0,5 điểm phần trăm dùng đúng mẫu số này. Không dùng lượng bán làm mẫu số vì can thiệp có thể tự làm thay đổi mẫu số đó.

---

# 4. Thiết kế kiến trúc tổng thể (25%)

## 4.1 Sơ đồ kiến trúc và luồng dữ liệu/điều khiển

{{architecture}}

## 4.2 Cơ sở lựa chọn kiến trúc

Quyết định đặt hàng hằng ngày phù hợp dự báo theo lô. Tệp nguồn lưu bền vững và thư viện tạo đặc trưng dùng chung giúp huấn luyện và suy luận nhất quán. Kho đăng ký lưu mô hình đã đánh giá; mỗi lần suy luận cố định một phiên bản đã duyệt, tránh đổi phiên bản giữa tác vụ khi bí danh thay đổi. Cơ sở dữ liệu dự báo tách lưu lượng API của nhân viên khỏi tác vụ huấn luyện và tạo đặc trưng tốn tài nguyên. Công bố nguyên tử ngăn người dùng thấy kết quả mới chỉ tính xong một phần.

Huấn luyện tách khỏi suy luận vận hành. Giám sát nhận dữ liệu thực tế trễ và kết quả đơn hàng; cảnh báo thay đổi phân bố tạo yêu cầu xem xét huấn luyện lại, không tự thay mô hình triển khai. Bổ sung hàng là quy tắc nghiệp vụ xác định dùng một mô hình nhu cầu, giữ độ phức tạp phù hợp đề bài.

## 4.3 Lịch vận hành hằng ngày (Asia/Bangkok)

| Thời gian | Hoạt động và trách nhiệm |
| --- | --- |
| 01:00 | Chốt nguồn; kỹ sư dữ liệu chịu trách nhiệm kiểm tra đủ tệp. |
| 01:00–02:00 | Thu thập, đối soát, kiểm tra; thử lại nguồn tự động một lần và cảnh báo sự cố. |
| 02:00–03:00 | Tạo đặc trưng đúng thời điểm ngày gốc; cố định ảnh chụp dữ liệu. |
| 03:00–03:30 | Dự báo bảy chân trời, kiểm tra đầu ra, tính đơn nháp. |
| 03:30–05:30 | Công bố hoặc khôi phục; đánh dấu dự phòng cho cặp không khả dụng; thông báo nhân viên. |
| Từ 06:00 | Nhân viên xem và duyệt; gửi bản nháp ERP bằng khóa chống trùng. |

---

# 4.4 Thành phần và các giai đoạn quy trình ML

| Thành phần, công cụ xem xét | Mục đích và trách nhiệm |
| --- | --- |
| Thu thập: tác vụ Python có lịch, tệp ERP/POS | Nhận biết phiên bản sửa nguồn; kiểm tra cấu trúc/khóa, đối soát; lưu danh mục tệp nguồn bất biến. |
| Lưu trữ: kho đối tượng mã hóa, Parquet | Tách vùng dữ liệu thô và đã xử lý; phân vùng theo ngày/cửa hàng; ảnh chụp và mã kiểm tra hỗ trợ xử lý lại. |
| Đặc trưng: Python, DuckDB/pandas | Tạo độ trễ, thống kê trượt, lịch, khuyến mãi đã biết, cờ sẵn có; dùng cùng mã cho ngày gốc lịch sử và hằng ngày. |
| Huấn luyện: LightGBM trên CPU | Một mô hình hồi quy cây tăng cường dùng chung với hàm mục tiêu Poisson phù hợp lượng đếm không âm [1]; xác thực siêu tham số, chặn âm rất nhỏ do số học và so sánh cơ sở. |
| Thí nghiệm và đăng ký: MLflow | Lưu mã, đặc trưng, danh mục dữ liệu, tham số và chỉ số; đăng ký ứng viên; đổi bí danh có người duyệt và cố định phiên bản [3]. |
| Điều phối: bộ lập lịch được quản lý hoặc Airflow sẵn có | Tác vụ ngày và huấn luyện ứng viên tuần; thử lại, phụ thuộc, lưu tiến độ/trạng thái. Ưu tiên nền tảng hiện có để giảm công bảo trì. |
| Cung cấp kết quả: PostgreSQL, FastAPI | Lưu dự báo/đề xuất theo lần chạy; API đọc có chỉ mục, phân quyền, con trỏ kết quả hiện hành và bản ghi duyệt. |
| Giao diện/tích hợp: trang nội bộ, API ERP | Giải thích đầu vào/lý do; lưu điều chỉnh có thể kiểm tra; gửi mỗi bản nháp đã duyệt một lần và đối soát phản hồi ERP. |
| Giám sát: Prometheus/Grafana hoặc công cụ hiện có | Cảnh báo tác vụ/thời hạn/lỗi; chất lượng nguồn, dự báo đủ dữ liệu thực tế và kết quả kinh doanh. |

## 4.5 Quy trình huấn luyện và phát hành

Thu thập tạo dữ liệu thô bất biến và danh mục nguồn. Kiểm tra tạo bảng theo ngày đã xử lý và vùng cách ly ngoại lệ. Tạo đặc trưng mở rộng ngày gốc theo chân trời và chỉ kết hợp dữ liệu hợp lệ tại ngày gốc. Huấn luyện loại nhãn bị hạn chế bởi hết hàng, lưu tiêu chí đủ điều kiện và lấy mẫu ngày gốc có thể tái lập khi cần. Xác thực báo cáo so sánh cơ sở, độ chệch, chất lượng từng nhóm và chi phí tính toán.

MLflow theo dõi tệp mô hình và phiên bản. Người duyệt kiểm tra khả năng tái lập và toàn bộ ngưỡng trước khi gán bí danh triển khai. Suy luận đọc bí danh một lần và lưu phiên bản cố định vào bản ghi lần chạy [3].

Tích hợp liên tục (CI) kiểm tra hợp đồng cấu trúc dữ liệu, phép kết hợp theo thời gian, cờ loại nhãn hết hàng, tính giống nhau giữa tạo đặc trưng lịch sử/hằng ngày và làm tròn đơn. Một bản phát hành đóng gói mô hình, cấu trúc đặc trưng và cấu hình. Từ chối phát hành khi cột, ánh xạ danh mục hoặc ý nghĩa nguồn không tương thích. Chạy lại ngày gốc lịch sử phải dùng dữ liệu lưu trữ và tệp mô hình tương ứng, không dùng danh mục đã sửa ở hiện tại. Đóng gói phụ thuộc và mã kiểm tra phiên bản mã giúp tái lập và khôi phục.

---

# 4.6 Độ tin cậy, giám sát và bảo trì

## Suy luận, công bố và tích hợp

Suy luận hằng ngày đọc một ảnh chụp đầu vào cố định và tính theo phân vùng cửa hàng. Lưu kết quả từng phân vùng theo run_id; tiếp tục phân vùng lỗi mà không ghi đè dữ liệu đã công bố. Kiểm tra đủ khóa/chân trời, tính duy nhất, dự báo hữu hạn và không âm, phiên bản mô hình và giá trị bất thường. Tạo đề xuất theo ảnh chụp tồn kho tương ứng. Chốt trọn bộ kết quả và đổi con trỏ lần chạy hiện hành trong một giao dịch cơ sở dữ liệu.

Phê duyệt lưu run_id mà nhân viên đã xem, tránh việc cập nhật dự báo âm thầm thay đổi đơn đã duyệt. Gửi ERP dùng khóa chống trùng gồm cửa hàng, nhà cung cấp, ngày xét đơn và phiên bản đã duyệt. Nếu phản hồi quá hạn, tra cứu ERP theo khóa trước khi thử lại. Sửa đơn tạo bản nháp thay thế rõ ràng. Thay đổi sản phẩm/giá không được bỏ qua ràng buộc nhà cung cấp.

## Tình huống lỗi và phương án dự phòng

| Tình huống | Cách xử lý vận hành |
| --- | --- |
| Thiếu POS hoặc không đạt chất lượng | Thử lại trong thời hạn, đánh dấu cửa hàng/cặp bị ảnh hưởng. Tính dự phòng mùa vụ từ lịch sử hợp lệ gần nhất và lịch đã xác nhận; hiển thị tuổi dữ liệu và trạng thái. |
| Suy luận hoặc kho mô hình không khả dụng | Dùng tệp đã duyệt lưu đệm nếu tương thích; nếu không, dùng quy tắc mùa vụ. Đầu vào lịch sử cũ quá 48 giờ thì đánh dấu không khả dụng và chuyển lập kế hoạch thủ công. |
| Tồn kho thiếu hoặc quá cũ | Có thể xem dự báo nhưng chặn xuất đơn đến khi sửa tồn kho hoặc nhân viên thực hiện quy trình ERP thủ công đã hướng dẫn. |
| API/cơ sở dữ liệu ngừng hoạt động | Chuyển sang bản sao API, khôi phục cơ sở dữ liệu; xuất CSV dự phòng có chữ ký/phiên bản. Ghi sự cố và khôi phục trong RTO. |
| Ứng viên suy giảm hoặc kết quả triển khai bất thường | Giữ mô hình hiện tại; khôi phục đồng bộ mô hình/đặc trưng/cấu hình, tính lại bản nháp chưa công bố, thông báo nhân viên. Đơn đã duyệt cần đối soát riêng. |

## Ngưỡng cảnh báo và đơn vị phụ trách

Đội vận hành nhận cảnh báo khi chưa công bố tại mốc dự kiến 03:30, lỗi dự báo/API tăng mạnh, nguồn không đạt chất lượng hoặc có nguy cơ trễ hạn; xác nhận tiếp nhận cảnh báo nghiêm trọng trong 15 phút. Kỹ sư dữ liệu điều tra khi độ đầy đủ dưới 99% hoặc tỷ lệ dòng hợp lệ dưới 99,5%.

Nhóm ML rà soát khi WAPE tuần đã có thực tế vượt 25%, độ chệch tuyệt đối vượt 5%, WAPE xấu hơn cơ sở trên 10% tương đối trong hai cửa sổ, hoặc phân bố đặc trưng thay đổi đáng kể. So sánh phân bố với tập huấn luyện bằng khoảng chia cố định; chỉ số ổn định quần thể (PSI) trên 0,2 là tín hiệu kinh nghiệm để điều tra, không phải bằng chứng tự động rằng độ chính xác đã giảm.

Chỉ đánh giá chân trời ngày thứ bảy khi đã có đủ dữ liệu thực tế. Tổng hợp chất lượng và tỷ lệ dự phòng hằng ngày; so sánh điều chỉnh, kết quả đơn và hết hàng hằng tuần. Lưu nhóm đủ điều kiện và nhóm bị loại để điểm tổng thể tốt không che khuất độ bao phủ thấp. Huấn luyện lại tuần tạo ứng viên; phát hành phải vượt các ngưỡng như lần đầu. Diễn tập khôi phục và rà soát phụ thuộc mỗi quý.

---

# 4.7 Cơ sở chọn mô hình và quy trình so sánh

## Các ứng viên đánh giá, một mô hình triển khai

| Phương án | Lợi thế và hạn chế trong bài toán | Vai trò quyết định |
| --- | --- | --- |
| Trung bình 28 ngày / cùng thứ bốn tuần | Ít tài nguyên, dễ giải thích; hạn chế với tương tác khuyến mãi. | Cơ sở bắt buộc và dự phòng; đo thực tế trước khi kết luận ML cần thiết. |
| ETS theo chuỗi, mùa vụ tuần | Biểu diễn mức, xu hướng, mùa vụ với cấu trúc thống kê; cần đủ lịch sử hợp lệ và quản lý nhiều chuỗi. | Cơ sở thống kê bổ sung trên cùng tập đủ điều kiện; ghi tỷ lệ không hội tụ và quy tắc dự phòng. |
| LightGBM dùng chung, có chân trời | Khai thác tương tác và dữ liệu giữa chuỗi, hỗ trợ đặc trưng dạng bảng; cần kiểm soát rò rỉ và sai nhóm. | Ứng viên MVP; chỉ triển khai nếu vượt các cơ sở và đáp ứng thời hạn. |
| Mô hình chuỗi học sâu | Có thể khai thác quan hệ thời gian; tăng công điều chỉnh, tài nguyên và bảo trì. | Chưa đưa vào MVP; cần lợi ích và nguồn lực được chứng minh trước mở rộng. |

ETS dùng cùng nhãn/đặc trưng thời gian hợp lệ, không nội suy bằng dữ liệu tương lai. Chuỗi có khoảng trống được xử lý thiếu theo thư viện đã kiểm chứng; không giả vờ ngày hết hàng là nhãn nhu cầu đầy đủ. Mọi phương án thiếu hỗ trợ một chuỗi đều dùng cùng quy tắc dự phòng và công bố độ bao phủ. Bổ sung ứng viên để so sánh không làm kiến trúc triển khai có nhiều mô hình tương tác.

## Hàm mục tiêu và ý nghĩa dự báo

Mô hình dự báo kỳ vọng có điều kiện μ(x,h) = exp(g(x,h)) > 0. Hàm mất mát Poisson bỏ hằng số là trung bình [μ − y × log(μ)] trên các mẫu nhãn hợp lệ. Dùng trọng số chân trời bằng nhau; nếu lấy mẫu ngày gốc, lưu xác suất lấy mẫu và bảo đảm đại diện cửa hàng/chân trời. Không diễn giải lựa chọn hàm này thành bằng chứng nhu cầu thật tuân theo phân bố Poisson hoặc có phương sai bằng trung bình. Dữ liệu có thể quá phân tán; phải kiểm tra phần dư.

Poisson hướng đến kỳ vọng, trong khi sai số tuyệt đối/WAPE gắn với tối ưu trung vị. Báo cáo chọn dự báo kỳ vọng vì quy tắc bổ sung cần tổng nhu cầu, và dùng WAPE như chỉ số nghiệm thu dễ hiểu chứ không khẳng định hai mục tiêu tương đương. Nếu mất mát và quyết định không phù hợp, thử hàm hồi quy thay thế trong giai đoạn xác thực bằng cùng giao thức; chỉ giữ một ứng viên cuối cùng trước kiểm tra.

## So sánh công bằng và thử loại đặc trưng

Giới hạn đề xuất 20 cấu hình LightGBM trên các cửa sổ xác thực; ghi thời gian, cấu hình CPU và số luồng. Điều chỉnh độ sâu/số lá, tốc độ học và số cây; dùng dừng sớm chỉ trên xác thực, không trên kiểm tra cuối. Cơ sở mùa vụ cũng được điều chỉnh hệ số khuyến mãi trên huấn luyện. Chọn ứng viên bằng sai số, độ chệch, nhóm và thời gian, không chỉ WAPE tốt nhất.

Thử loại bỏ từng nhóm đặc trưng: không khuyến mãi; không đặc trưng cửa hàng/danh mục; không cờ sẵn có. Giữ cùng tập đánh giá và ngân sách để xác định thành phần có đóng góp thật. Báo cáo WAPE/MASE, thời gian và độ bao phủ của từng cấu hình, kể cả khi không cải thiện. Các phép thử này là kế hoạch, chưa có bảng kết quả thực nghiệm.

---

# 4.8 Bất định, tồn kho an toàn và tái lập

## Dự báo điểm không đủ biểu diễn rủi ro tồn kho

SS ban đầu là quy tắc đã duyệt, giữ nguyên giữa hai nhóm để hạn chế thay đổi không cần thiết. Trong giai đoạn xác thực, phân tích thêm phần dư tổng nhu cầu trên khoảng bảo vệ: e = tổng lượng bán đủ điều kiện − tổng dự báo cho cùng khoảng. Tổng phần dư phải lấy từ cùng ngày gốc và cùng quãng L+R; không cộng tùy tiện độ lệch chuẩn từng ngày như thể các sai số độc lập.

Có thể đề xuất SS = max(0, phân vị α của e), với α được nghiệp vụ chọn theo chi phí thiếu/dư. Kiểm tra α = 0,85/0,90/0,95 trên dữ liệu xác thực và mô phỏng tồn kho; đây là hiệu chỉnh thực nghiệm, không thêm mô hình ML. Không triển khai thay chính sách SS trong thử nghiệm chính nếu chưa duyệt và xác lập lại gói can thiệp. Nhóm ít phần dư dùng quy tắc đã duyệt hoặc nhóm danh mục tương đồng có nêu giới hạn.

Phần dư loại ngày hết hàng không thể cung cấp bảo đảm bao phủ cho nhu cầu tiềm ẩn mọi ngày; không tuyên bố mức α tương đương tỷ lệ ngày không hết hàng. Cần dữ liệu thời điểm sẵn có và kiểm chứng thực tế trước khi sử dụng diễn giải xác suất. Các giới hạn về nhãn và tham số chính sách phải xuất hiện cạnh kết quả, không chỉ trong phụ lục.

## Vòng phản hồi và nợ kỹ thuật

Sculley và cộng sự mô tả rủi ro phụ thuộc dữ liệu và vòng phản hồi ẩn trong hệ thống ML [8]. Ở bài này, dự báo đổi đơn, đơn đổi tình trạng có hàng và lượng bán, rồi lượng bán trở thành nhãn mới. Vì vậy, lưu chính sách/phiên bản đơn cùng dữ liệu bán; giám sát sự thay đổi độ bao phủ và cờ hết hàng sau triển khai. Không coi mọi thay đổi lượng bán sau dùng ML là thay đổi sở thích khách hàng.

## Gói bằng chứng cho một lần phát hành

| Bằng chứng cần lưu | Điều kiện kiểm tra |
| --- | --- |
| Danh mục nguồn, available_at, mã kiểm tra, mặt nạ nhãn | Tái tạo đúng thông tin đã biết tại ngày gốc. |
| Mã, phụ thuộc, tham số, hạt giống và tài nguyên | Chạy lại tái lập sai số trong sai khác số học được xác định trước. |
| Kết quả từng cơ sở/ứng viên, từng cửa sổ và nhóm | Cùng tập đánh giá; có độ bao phủ và lý do loại mẫu. |
| Kiểm thử thời gian, dự phòng, đơn trùng và khôi phục | Có kịch bản, người chịu trách nhiệm và bằng chứng đạt/chưa đạt. |
| Biên bản duyệt, phiên bản mô hình/đặc trưng/chính sách | Có người duyệt và phiên bản có thể khôi phục đồng bộ. |

Thứ tự triển khai là khảo sát và đo cơ sở → phát lại lịch sử → quan sát hai tuần → thử nghiệm có đối chứng → mở rộng có duyệt. Ở mỗi bước, thất bại giữ hệ thống tại bước hiện tại hoặc quay về chính sách cơ sở; không thay số liệu thiếu bằng kết quả giả định. Đây là điều kiện quản trị để thiết kế có thể bảo vệ bằng bằng chứng.

---

# 5. Phân tích các đánh đổi (15%)

| Đánh đổi | Lựa chọn và hệ quả | Quyết định và điều kiện xem xét lại |
| --- | --- | --- |
| Độ chính xác và độ trễ | Quy tắc mùa vụ rẻ, dễ hiểu nhưng bỏ sót tác động khuyến mãi phi tuyến. Cây tăng cường có thể giảm sai số với chi phí đặc trưng/huấn luyện tăng; mô hình chuỗi học sâu tăng công tính toán và điều chỉnh. | Dùng một LightGBM trên CPU, giữ dự phòng mùa vụ. Chỉ tăng độ phức tạp khi cải thiện WAPE/nhóm và lợi ích thử nghiệm đủ bù chi phí, vẫn đạt thời gian xử lý. |
| Độ mới dữ liệu và chi phí | Dữ liệu bán/tồn kho theo luồng có thể phản ứng trong ngày nhưng cần hạ tầng sự kiện và hỗ trợ vận hành. Ảnh chụp ngày có thể bỏ lỡ thay đổi sau giờ chốt. | Dự báo theo lô ngày vì xét đơn theo ngày. Hiển thị thời điểm chốt, dùng tồn kho đã xác nhận lúc duyệt; xem xét cập nhật trong ngày nếu biến động muộn thường xuyên gây hại. |
| Đơn giản và hiệu năng | Mô hình chung chia sẻ dữ liệu, dễ phát hành. Mô hình riêng theo sản phẩm/danh mục có thể khớp cục bộ hơn nhưng tăng số tệp, khó xử lý chuỗi thưa và công bảo trì. | Dùng mô hình chung với đặc trưng cửa hàng/danh mục và ngưỡng từng nhóm; loại nhóm chưa hỗ trợ. Chỉ xem xét tách mô hình khi suy giảm nhóm quan trọng kéo dài, không sửa được trong mô hình chung. |
| Tự động hóa và quyền kiểm soát | Tự đặt ERP giảm lao động nhưng có thể khuếch đại dữ liệu sai hoặc tăng nhu cầu bất thường. Duyệt thủ công thêm công và tạo khác biệt can thiệp. | Chỉ tạo đơn nháp, yêu cầu lý do sửa và hiển thị cảnh báo dự phòng/ràng buộc. Xem xét duyệt tự động có giới hạn sau kết quả thử nghiệm ổn định và được kinh doanh cho phép. |
| Quyền riêng tư và độ chi tiết dữ liệu | Lịch sử khách hàng/giỏ hàng có thể bổ sung tín hiệu nhưng tăng rủi ro định danh và công quản trị. Dữ liệu ngày tổng hợp mất thông tin cá nhân. | Chỉ dùng dữ liệu cửa hàng–sản phẩm tổng hợp; bổ sung hàng không cần cá nhân hóa. Xem xét tín hiệu tổng hợp mới sau đánh giá độ chính xác/chi phí, không mặc định cần định danh. |

## 5.1 Rủi ro còn lại và nguyên tắc quyết định

Bất định chính là nhu cầu không quan sát được khi hết hàng: loại ngày hết hàng có thể làm tập huấn luyện thiên về ngày đủ hàng. Đối soát tồn kho và thử nghiệm kinh doanh có đối chứng đáng tin cậy hơn việc tự tạo nhãn lượng bán bị mất. Sản phẩm mới và chuỗi quá thưa chỉ dùng dự phòng. Khuyến mãi hoặc nhà cung cấp thay đổi đột ngột có thể vượt phân bố huấn luyện; cần ràng buộc, chỉ báo độ mới và người duyệt.

Điều chỉnh lớn có thể giúp đơn hàng nhưng làm khó việc quy kết lợi ích kinh doanh cho mô hình; giữ cả dự báo và quyết định. Ngân sách 500 USD/tháng là ràng buộc đề xuất, không phải báo giá đám mây. Đối chiếu dung lượng, giờ CPU, độ sẵn sàng cơ sở dữ liệu và giám sát với báo giá mua sắm thực tế; tính riêng công hỗ trợ. Chỉ áp dụng thành phần đạt nghiệm thu và có giá trị. Nếu cơ sở tốt hơn hoặc thử nghiệm chưa rõ, giữ chính sách hiện tại và ghi bằng chứng.

---

# Tài liệu tham khảo và đối chiếu yêu cầu

## Tài liệu kỹ thuật

[A] Đề bài: INDIVIDUAL ASSIGNMENT 1_baiCaNhan.pdf, cung cấp trong thư mục dự án, 3 trang. Các mục I–IV quy định đặc điểm bài toán, nội dung báo cáo, tỷ trọng và cách đặt tên tệp.

[1] LightGBM, tài liệu Parameters chính thức; các hàm mục tiêu, bao gồm Poisson. https://lightgbm.readthedocs.io/en/latest/Parameters.html. Truy cập ngày 03/10/2026. Nguồn xác nhận khả năng thuật toán, không chứng minh mức cải thiện giả định.

[2] scikit-learn, tài liệu TimeSeriesSplit chính thức. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html. Truy cập ngày 03/10/2026. Nguồn hỗ trợ chia tập theo thời gian và khoảng cách giữa tập; quy tắc gom ngày gốc và loại nhãn chồng lấn trong báo cáo là quyết định thiết kế cho bài toán.

[3] MLflow, tài liệu Model Registry Workflows chính thức. https://www.mlflow.org/docs/latest/ml/model-registry/workflow/. Truy cập ngày 03/10/2026. Nguồn hỗ trợ vòng đời phiên bản/bí danh mô hình; các ngưỡng vận hành trong báo cáo là yêu cầu đề xuất.

## Nghiên cứu và phương pháp học thuật

[4] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013.

[5] Ma, S., & Fildes, R. (2022). The performance of the global bottom-up approach in the M5 accuracy competition: A robustness check. International Journal of Forecasting, 38(4), 1492–1499. https://doi.org/10.1016/j.ijforecast.2021.09.002. Bản tác giả: https://eprints.lancs.ac.uk/id/eprint/159736/.

[6] Hewamalage, H., Ackermann, K., & Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. Data Mining and Knowledge Discovery, 37, 788–832. https://doi.org/10.1007/s10618-022-00894-5.

[7] Jain, A., Rudi, N., & Wang, T. (2015). Demand Estimation and Ordering Under Censoring: Stock-Out Timing Is (Almost) All You Need. Operations Research, 63(1), 134–150. Bản bài báo tại NUS: https://web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/6isNE1485323583.pdf.

[8] Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F., & Dennison, D. (2015). Hidden Technical Debt in Machine Learning Systems. Advances in Neural Information Processing Systems, 28. https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html.

[9] Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3rd ed.), mục 5.8, Evaluating point forecast accuracy. OTexts. https://otexts.com/fpp3/accuracy.html.

[10] Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3rd ed.), mục 5.10, Time series cross-validation. OTexts. https://otexts.com/fpp3/tscv.html.

[11] Campbell, M. K., Piaggio, G., Elbourne, D. R., & Altman, D. G., for the CONSORT Group. (2012). CONSORT 2010 statement: Extension to cluster randomised trials. BMJ, 345, e5661. https://doi.org/10.1136/bmj.e5661.

Các nguồn trực tuyến được kiểm tra ngày 03/10/2026. Trích dẫn đánh số để liên kết luận điểm với nguồn; kết quả của nghiên cứu được phân biệt với giả định và quyết định đề xuất cho hệ thống này. Không sao chép kết quả nghiên cứu thành kết quả thực nghiệm của báo cáo.

---

# Đối chiếu yêu cầu và kết luận thiết kế

## Đối chiếu độ đầy đủ với PDF đề bài

| Yêu cầu trong PDF | Nội dung đáp ứng |
| --- | --- |
| Bài toán ML; ít nhất hai bên liên quan; triển khai thực tế; dữ liệu hợp lý; tác động đo được | Mục 1.1–1.8, 2.5 và 3.1–3.3; chuỗi bán lẻ giả định, sáu nhóm liên quan, một mô hình ML. |
| Định nghĩa bài toán (20%): bối cảnh, phát biểu, hiện trạng, lý do chọn ML, các bên liên quan | Mục 1.1–1.8. |
| Phân tích yêu cầu (20%): chức năng, đầu vào/đầu ra, tích hợp, tương tác người dùng | Mục 2.1–2.3; duyệt đơn, hợp đồng ERP và nguồn gốc dữ liệu. |
| Phi chức năng: độ trễ, mở rộng, tin cậy, bảo trì; dữ liệu: nguồn, chất lượng, riêng tư, khối lượng | Mục 2.4–2.5 và 4.6. |
| Mục tiêu/chỉ số (20%): kinh doanh, hệ thống, mô hình, ngưỡng và đường cơ sở | Mục 3.1–3.5; công thức, cơ sở ngưỡng, độ nhạy kinh tế, cỡ mẫu và kế hoạch phân tích. |
| Kiến trúc (25%): sơ đồ rõ, luồng dữ liệu, giai đoạn ML, trách nhiệm và công cụ | Mục 4.1–4.8: quy trình, giám sát, khôi phục, so sánh mô hình, bất định và tái lập. |
| Đánh đổi (15%): ít nhất 3–4 quyết định quan trọng | Phần 5 phân tích năm đánh đổi, lựa chọn và điều kiện xem xét lại. |
| Tên tệp: DDM501_Assignment1_[StudentID]_[Name].pdf | DDM501_Assignment1_{{student_id}}_{{name}}.pdf; khoảng trắng trong họ tên được thay bằng dấu gạch dưới. |

## Kết luận thiết kế

Thiết kế lựa chọn một mô hình dự báo dùng chung, quy trình xử lý theo lô và phê duyệt đơn có người kiểm soát. Cơ sở lựa chọn gồm bằng chứng nghiên cứu, ràng buộc doanh nghiệp và các phép kiểm chứng được xác định trước. Dự báo và đơn hàng liên kết bằng quy ước thời gian, tồn kho theo ETA và phiên bản chính sách, giúp kiểm tra tính nhất quán từ dữ liệu đến quyết định.

Thiết kế chưa chứng minh hiệu quả. Điều kiện quan trọng trước triển khai là chất lượng nhãn, độ bao phủ, năng lực vận hành và đủ số cửa hàng cho kết luận thống kê. Chỉ mở rộng khi dữ liệu kiểm tra, thử nghiệm kinh doanh và tính toán chi phí cùng ủng hộ quyết định; nếu không, phương pháp cơ sở tiếp tục là lựa chọn hợp lệ. Các giả thuyết có thể bị bác bỏ và các giới hạn được công bố là nền tảng để bảo vệ thiết kế bằng lập luận học thuật.

## Điều kiện chấp nhận và phần việc chưa thực hiện

Yêu cầu đề bài được đáp ứng ở mức tài liệu thiết kế. Chưa thực hiện thu thập dữ liệu thực, huấn luyện, kiểm thử tải, mô phỏng tồn kho hoặc thử nghiệm tại cửa hàng. Vì vậy, mọi ngưỡng là điều kiện cần kiểm chứng, không phải chứng nhận hệ thống đã đạt. Các mục tiêu không được thay đổi sau khi xem kết quả chỉ để làm thiết kế có vẻ thành công.

Trước xây dựng, cần hoàn thành bốn quyết định: xác nhận hợp đồng và chất lượng dữ liệu; ký duyệt ngưỡng nghiệp vụ cùng cách đo; xác định cấu hình và ngân sách bằng báo giá; chốt giao thức thử nghiệm đủ sức mạnh thống kê. Nếu một quyết định chưa khả thi, cập nhật phạm vi có lý do và ghi rõ tác động đến giả thuyết. Tính chặt chẽ của báo cáo nằm ở khả năng kiểm tra, bác bỏ và sửa quyết định bằng bằng chứng.

## Ghi chú nộp bài

Đây là tài liệu thiết kế, chưa phải hệ thống đã triển khai hoặc xác thực thực nghiệm. Giữ nhãn giả định cho số liệu chưa đo. Thông tin sinh viên: {{student_id}} – {{name}}. Bản Word và Markdown phục vụ chỉnh sửa; PDF là định dạng nộp theo đề bài.
