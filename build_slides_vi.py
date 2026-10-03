"""Generate a concise 16:9 Vietnamese presentation from the design report."""
from pathlib import Path
import json
import math
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import pymupdf
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'deliverables'/'tieng_viet'/'slides'
OUT.mkdir(exist_ok=True)
student=json.loads((ROOT/'student.json').read_text(encoding='utf-8'))
stem='DDM501_Assignment1_25MS13312_Nguyen_Minh_Truong_Slides'
for name,filename in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/filename)))
W,H=960,540
NAVY='#12384A';TEAL='#087F82';INK='#263E4A';MUTED='#536B76';BG='#F5F7F4';LINE='#CBD9D8';MINT='#E0EFEB';WHITE='#FFFFFF'
pdf=OUT/(stem+'.pdf')
c=canvas.Canvas(str(pdf),pagesize=(W,H))
c.setTitle('DDM501 – Tóm tắt thiết kế hệ thống dự báo nhu cầu')
c.setAuthor(student['name'])
outline=[]
errors=[]
total=14
current=0

def rect(x,y,w,h,fill,stroke=None,radius=12):
    c.setFillColor(colors.HexColor(fill))
    c.setStrokeColor(colors.HexColor(stroke or fill))
    c.roundRect(x,y,w,h,radius,fill=1,stroke=bool(stroke))

def text(s,x,y,width,size=20,color=INK,bold=False,max_height=None,align=0):
    style=ParagraphStyle('slide',fontName='Arial-Bold' if bold else 'Arial',fontSize=size,leading=size*1.28,textColor=colors.HexColor(color),alignment=align)
    p=Paragraph(escape(s).replace('\n','<br/>'),style)
    _,height=p.wrap(width,1000)
    if max_height and height>max_height:
        errors.append(f'Slide {current}: text exceeds allocated height: {s[:50]}')
    if y-height<35 and size>10:
        errors.append(f'Slide {current}: text enters footer: {s[:50]}')
    p.drawOn(c,x,y-height)
    outline.append(s)
    return height

def slide(title,kicker):
    global current
    current+=1
    c.setFillColor(colors.HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
    rect(40,482,42,5,TEAL,radius=2)
    text(kicker.upper(),94,492,825,11,TEAL,bold=True,max_height=18)
    text(title,40,466,880,29,NAVY,bold=True,max_height=76)
    c.setStrokeColor(colors.HexColor(LINE));c.line(40,38,920,38)
    text(f'DDM501  •  {student["student_id"]}  •  {student["name"]}',40,28,800,10,MUTED)
    text(f'{current:02d} / {total}',850,28,70,10,MUTED,align=2)
    c.bookmarkPage(f'slide-{current}');c.addOutlineEntry(title,f'slide-{current}',level=0)
    outline.append('\n## '+str(current)+'. '+title)

def end():c.showPage()

def card(x,y,w,h,label,body,accent=TEAL,size=19):
    rect(x,y,w,h,WHITE,LINE)
    rect(x+18,y+h-28,26,4,accent,radius=2)
    text(label,x+18,y+h-44,w-36,18,accent,bold=True,max_height=55)
    body_offset=94 if h<=160 else 103
    text(body,x+18,y+h-body_offset,w-36,size,max_height=h-body_offset-6)

def banner(s,y=62):
    rect(40,y,880,54,MINT)
    text(s,57,y+42,846,17,NAVY,max_height=43)

def bullets(items,x=40,y=390,w=880,size=21,gap=16):
    for item in items:
        rect(x,y-17,6,6,TEAL,radius=2)
        height=text(item,x+20,y,w-20,size,max_height=100)
        y-=height+gap

def arrow(x1,y1,x2,y2,label=None):
    c.setStrokeColor(colors.HexColor(TEAL));c.setLineWidth(1.7);c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1)
    for off in [-.5,.5]:c.line(x2,y2,x2-7*math.cos(a+off),y2-7*math.sin(a+off))
    if label:text(label,min(x1,x2)+5,max(y1,y2)+20,180,12,MUTED)

# 1
slide('Dự báo nhu cầu hàng hóa\ncho chuỗi bán lẻ','Bài tập cá nhân 1 • ML System Design')
text('Một mô hình dùng chung.\nĐề xuất bổ sung hàng có người phê duyệt.',40,339,870,25,TEAL,bold=True,max_height=75)
text('Nguyễn Minh Trường  |  MSSV: 25MS13312\nHọc phần DDM501 – AI in DevOps, DataOps, MLOps',40,235,870,21,max_height=64)
banner('Tài liệu thiết kế: số liệu và mục tiêu là giả định; chưa có kết quả thực nghiệm.',y=91)
text('Bản tóm tắt phục vụ thuyết trình • Báo cáo tiếng Việt phiên bản 2.1',40,76,875,15,MUTED)
end()

# 2
slide('Bài toán: giảm hết hàng và tồn kho dư','01 • Định nghĩa bài toán')
card(40,164,280,235,'BỐI CẢNH','20 cửa hàng\n2.000 sản phẩm/cửa hàng\nGiao hàng sau 1–3 ngày',size=21)
card(340,164,280,235,'HIỆN TRẠNG','Trung bình bán 28 ngày\nBảng tính và chỉnh tay\nThiếu đánh giá thống nhất',size=20)
card(640,164,280,235,'GIÁ TRỊ KỲ VỌNG','Giảm thiếu hàng\nGiảm vốn tồn kho\nGiảm thời gian lập đơn',size=21)
banner('Phạm vi: mặt hàng có lịch sử ổn định; sản phẩm mới hoặc quá gián đoạn dùng dự phòng.')
end()

# 3
slide('Các bên liên quan và xung đột mục tiêu','01 • Stakeholders')
card(40,253,430,150,'CỬA HÀNG / LẬP KẾ HOẠCH','Có hàng để bán; hiểu đề xuất và được điều chỉnh.',size=18)
card(490,253,430,150,'KINH DOANH / TÀI CHÍNH','Giảm tồn kho; lợi ích phải bù chi phí.',size=18)
card(40,88,430,150,'DỮ LIỆU / ML','Nhãn đáng tin; so sánh công bằng; tái lập được.',size=18)
card(490,88,430,150,'VẬN HÀNH / MUA HÀNG / AN NINH','Kịp hạn; đơn khả thi; phân quyền và truy vết.',size=18)
end()

# 4
slide('Yêu cầu hệ thống: đủ chức năng, kịp thời hạn','02 • Yêu cầu chức năng và phi chức năng')
card(40,154,430,250,'CHỨC NĂNG','Dự báo 7 ngày theo cửa hàng–SKU\nTạo đơn nháp và duyệt trên giao diện\nTích hợp POS/ERP; lưu phiên bản\nChống đơn trùng; có dự phòng',size=18)
card(490,154,430,250,'NGƯỠNG ĐỀ XUẤT','40.000 cặp → 280.000 dòng/ngày\nCông bố trước 05:30\nSuy luận p95 ≤ 30 phút\nAPI p95 ≤ 500 ms tại 20 yêu cầu/giây',size=18)
banner('Đúng hạn ≥ 99% ngày; API sẵn sàng ≥ 99,5%/tháng. Các ngưỡng cần kiểm thử tải.')
end()

# 5
slide('Dữ liệu: chất lượng quan trọng hơn số lượng','02 • Nguồn dữ liệu và quyền riêng tư')
card(40,154,430,250,'NGUỒN VÀ KHỐI LƯỢNG','POS, tồn kho, danh mục sản phẩm\nGiá và khuyến mãi đã xác nhận\n18 tháng ≈ 21,92 triệu dòng ngày\nLưu thời điểm dữ liệu có sẵn',size=18)
card(490,154,430,250,'KIỂM SOÁT','Không coi tệp thiếu là bán bằng 0\nLoại nhãn ngày hết hàng khỏi ML\nKhông thu thập định danh khách hàng\nMã hóa, phân quyền, lưu có thời hạn',size=18)
banner('Lượng bán khi hết hàng không phản ánh đủ nhu cầu [6]; phải báo cáo thiên lệch và độ bao phủ.')
end()

# 6
slide('Vì sao chọn một LightGBM dùng chung?','03 • Cơ sở học thuật và lựa chọn mô hình')
card(40,147,280,258,'PHƯƠNG PHÁP CƠ SỞ','Trung bình 28 ngày\nCùng thứ trong 4 tuần\nETS theo chuỗi\n\nBắt buộc so sánh công bằng.',size=18)
card(340,147,280,258,'ỨNG VIÊN ML','Học tương tác lịch/giá\nChia sẻ dữ liệu giữa chuỗi\nĐặc trưng + chân trời\n\nMột mô hình cuối cùng.',size=18)
card(640,147,280,258,'GIỚI HẠN','M5 hỗ trợ chọn ứng viên [1]\nHiệu năng có thể đổi theo kỳ [2]\n\nKhông mặc định ML sẽ thắng.',size=18)
banner('Poisson dự báo kỳ vọng; WAPE là chỉ số nghiệm thu. Không giả định nhu cầu thật có phân bố Poisson.')
end()

# 7
slide('Kiến trúc: tách huấn luyện và vận hành','04 • Luồng dữ liệu và kiểm soát')
nodes=[(40,294,'NGUỒN DỮ LIỆU','POS / ERP / Khuyến mãi'),(350,294,'KIỂM TRA + ĐẶC TRƯNG','Ảnh chụp có phiên bản'),(660,294,'HUẤN LUYỆN TUẦN','Đánh giá → duyệt → MLflow'),(40,156,'SUY LUẬN THEO LÔ','Dự báo + quy tắc đặt hàng'),(350,156,'CÔNG BỐ NGUYÊN TỬ','PostgreSQL → API'),(660,156,'NHÂN VIÊN + ERP','Điều chỉnh → duyệt đơn')]
for x,y,label,body in nodes:
    rect(x,y,260,86,WHITE,LINE)
    text(label,x+14,y+69,232,16,TEAL,bold=True,max_height=24)
    text(body,x+14,y+40,232,16,max_height=44)
arrow(300,337,350,337);arrow(610,337,660,337)
arrow(480,294,480,270);arrow(480,270,170,270);arrow(170,270,170,242)
arrow(790,294,790,256);arrow(790,256,210,256);arrow(210,256,210,242)
arrow(300,199,350,199);arrow(610,199,660,199)
banner('Giám sát dữ liệu, thực tế và đơn hàng → điều tra → ứng viên mới; phát hành luôn có người duyệt.')
text('Phiên bản mô hình được cố định cho mỗi lần chạy; lưu dữ liệu/mã/chính sách để khôi phục [4].',40,132,880,16,MUTED)
end()

# 8
slide('Từ dự báo đến đơn hàng: đúng thời điểm','04 • Chính sách bổ sung hàng')
text('Sáng ngày D: dữ liệu đến D−1 → dự báo D…D+6',40,397,880,23,TEAL,bold=True,max_height=35)
text('Khoảng bảo vệ = thời gian giao L + chu kỳ xét đơn R\nIP = hàng hiện có + hàng về đúng khoảng − giữ chỗ độc lập\nS = tổng dự báo trong khoảng bảo vệ + tồn kho an toàn',40,339,880,21,max_height=99)
rect(40,169,880,63,MINT)
text('Q = p × ceil(max(0, S − IP) / p)',60,216,835,25,NAVY,bold=True,max_height=36)
text('Ví dụ giả định: L=2, R=1, S=70, IP=40, kiện p=6 → đặt 30 đơn vị.',40,149,880,19,max_height=28)
text('Kiểm tra hàng về theo ETA; thiếu trước ngày giao cần ngoại lệ giao gấp/chuyển hàng.',40,101,880,18,MUTED,max_height=47)
end()

# 9
slide('Mục tiêu: từ kinh doanh đến mô hình','03 • Các ngưỡng đề xuất, không phải kết quả')
for x,label,before,after in [(40,'HẾT HÀNG','8%','≤ 6,4%'),(340,'NGÀY TỒN KHO','12 ngày','≤ 10,8 ngày'),(640,'GIỜ/CỬA HÀNG/TUẦN','4 giờ','≤ 2,5 giờ')]:
    rect(x,224,280,177,WHITE,LINE)
    text(label,x+18,379,244,17,TEAL,bold=True,max_height=28)
    text(before+' →',x+18,335,244,24,MUTED,max_height=33)
    text(after,x+18,291,244,30,NAVY,bold=True,max_height=43)
text('Mô hình: WAPE ≤ 25% VÀ giảm tương đối ≥ 10% so với cơ sở tốt nhất.\nĐộ chệch tuyệt đối ≤ 5%; kiểm tra sai số từng nhóm và MASE.',40,201,880,20,max_height=60)
banner('Cơ sở là giả định cần đo lại. Chất lượng dự báo tốt chưa đủ chứng minh lợi ích kinh doanh.')
end()

# 10
slide('Đánh giá ngoại tuyến: không rò rỉ tương lai','03 • Thiết kế kiểm chứng dự báo')
for x,w,title,body in [(40,390,'THÁNG 1–12','Huấn luyện ban đầu'),(446,218,'THÁNG 13–15','3 lượt xác thực tiến dần'),(680,240,'THÁNG 16–18','Kiểm tra chưa dùng chọn')]:
    rect(x,291,w,108,MINT if x==680 else WHITE,LINE)
    text(title,x+16,377,w-32,19,TEAL,bold=True,max_height=30)
    text(body,x+16,339,w-32,18,max_height=50)
bullets(['Giữ thứ tự thời gian; loại nhãn huấn luyện chồng cửa sổ tương lai.','Đặc trưng chỉ dùng thông tin đã biết tại thời điểm chốt.','So sánh cùng mẫu: WAPE, MAE/MASE, độ chệch và độ bao phủ.'],x=40,y=260,w=880,size=20,gap=14)
text('Khung đánh giá dựa trên nghiên cứu về sai sót đánh giá dự báo [3] và xác thực chuỗi thời gian [5].',40,96,880,16,MUTED,max_height=44)
end()

# 11
slide('Thử nghiệm kinh doanh: cửa hàng là đơn vị mẫu','03 • Pilot và độ tin cậy thống kê')
card(40,167,430,235,'KẾ HOẠCH SƠ BỘ','2 tuần chạy quan sát\n8 tuần thử nghiệm, 10 cặp cửa hàng\nNgẫu nhiên trong từng cặp\nPhân tích theo nhóm phân ban đầu',size=18)
card(490,167,430,235,'ĐIỀU KIỆN KẾT LUẬN','Đo chênh lệch trước–sau theo cặp\nKhoảng tin cậy 95%; kiểm tra độ bền\nGiữ giới hạn tồn kho và hao hụt\nTheo dõi ảnh hưởng giữa cửa hàng',size=18)
banner('10 cặp chưa chắc đủ phát hiện giảm 1,6 điểm phần trăm: cần tính cỡ mẫu trước khi chốt kế hoạch.')
end()

# 12
slide('Các đánh đổi: quyết định có điều kiện','05 • Trade-offs')
rows=[('Độ chính xác ↔ độ trễ','LightGBM trên CPU; giữ phương pháp cơ sở.'),('Độ mới ↔ chi phí','Theo lô hằng ngày; chỉ nâng tần suất khi có bằng chứng.'),('Đơn giản ↔ hiệu năng','Một mô hình chung; giám sát theo nhóm.'),('Tự động hóa ↔ kiểm soát','Đơn nháp có người duyệt và lưu lý do sửa.'),('Riêng tư ↔ độ chi tiết','Dữ liệu tổng hợp; không cần định danh khách hàng.')]
y=395
for label,decision in rows:
    rect(40,y-52,880,57,WHITE,LINE,radius=7)
    text(label,55,y-6,300,17,TEAL,bold=True,max_height=45)
    text(decision,370,y-6,529,17,max_height=45)
    y-=65
end()

# 13
slide('Chỉ mở rộng khi bằng chứng và kinh tế cùng đạt','Kết luận • Điều kiện triển khai')
card(40,158,430,243,'KINH TẾ MINH HỌA','Hạ tầng: 500 USD/tháng\nHỗ trợ: 160 USD/tháng\nLợi ích giả định: 950 USD/tháng\nRòng: +290; giảm nửa lợi ích → −185',size=18)
card(490,158,430,243,'QUYẾT ĐỊNH','Dữ liệu đủ tốt, mô hình vượt cơ sở\nHệ thống đạt thời hạn và khôi phục\nPilot cải thiện, không phá giới hạn\nLợi ích ròng dương sau hỗ trợ',size=18)
banner('Chưa có dữ liệu thực hoặc kết quả huấn luyện. Nếu bằng chứng chưa đạt, tiếp tục dùng cơ sở.')
end()

# 14
slide('Nguồn chính và thông điệp cuối','Tài liệu tham khảo • Số thứ tự riêng cho slide')
references=[
('[1] Makridakis và cs. (2022). M5 accuracy competition.','https://doi.org/10.1016/j.ijforecast.2021.11.013'),
('[2] Ma & Fildes (2022). M5: A robustness check.','https://doi.org/10.1016/j.ijforecast.2021.09.002'),
('[3] Hewamalage và cs. (2023). Forecast evaluation: Common pitfalls.','https://doi.org/10.1007/s10618-022-00894-5'),
('[4] Sculley và cs. (2015). Hidden Technical Debt in ML Systems.','https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html'),
('[5] Hyndman & Athanasopoulos (2021). Forecasting: Principles and Practice.','https://otexts.com/fpp3/tscv.html'),
('[6] Jain, Rudi & Wang (2015). Demand Estimation and Ordering Under Censoring.','https://web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/6isNE1485323583.pdf')]
y=399
for label,url in references:
    text(label,40,y,880,17,max_height=27)
    c.linkURL(url,(40,y-23,920,y),relative=0,thickness=0)
    y-=38
text('Nguồn chi tiết và giả định: báo cáo tiếng Việt phiên bản 2.1.\nBấm vào tên tài liệu để mở nguồn.',40,154,880,16,MUTED,max_height=46)
banner('Đóng góp của bài: thiết kế có thể kiểm chứng; hiệu quả thực tế phải được xác nhận trước mở rộng.')
end()

assert current==total
assert not errors, '\n'.join(errors)
c.save()
(OUT/'NOI_DUNG_SLIDE.md').write_text('# Tóm tắt thuyết trình DDM501\n\n'+'\n\n'.join(outline),encoding='utf-8')

report=pymupdf.open(pdf)
assert len(report)==total
violations=[]
thumbs=[]
for index,page in enumerate(report):
    content=page.get_text()
    assert '\ufffd' not in content and '\u25a0' not in content
    assert page.rect.width==W and page.rect.height==H
    for block in page.get_text('blocks'):
        if block[0]<30 or block[1]<20 or block[2]>930 or block[3]>H-10:
            violations.append({'slide':index+1,'text':block[4][:100],'bounds':block[:4]})
    pix=page.get_pixmap(matrix=pymupdf.Matrix(.5,.5))
    thumbs.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
sheet=Image.new('RGB',(3*490,math.ceil(total/3)*295),'#DCE5E3')
draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%3)*490+5;y=(i//3)*295+5
    sheet.paste(im,(x,y));draw.text((x,y+272),f'Slide {i+1}',fill='#12384A')
sheet.save(OUT/'slide_preview.png')
result={'slides':total,'aspect_ratio':'16:9','vietnamese_glyphs':'PASS','allocated_text_heights':'PASS','layout_violations':violations,'references_linked':len(report[-1].get_links()),'status':'PASS' if not violations else 'REVIEW'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
assert not violations
