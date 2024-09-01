# Face-recognition&Scoring
**I.Giới Thiệu về dự án**
- Face-recognition&Scoring là công nghệ nhận diện khuôn mặt dựa trên các đặc điểm sinh trắc học. Công nghệ này sử dụng các thuật toán để phân tích các đặc trưng trên khuôn mặt, như khoảng cách giữa mắt, hình dáng mũi, và cấu trúc xương hàm, từ đó xác định danh tính của người dùng. Chấm điểm khuôn mặt là quá trình đánh giá và cho điểm các đặc điểm khuôn mặt dựa trên các tiêu chí thẩm mỹ hoặc sinh trắc học. Điểm số này có thể được sử dụng trong nhiều ứng dụng, từ xác thực danh tính đến phân tích tâm lý học hành vi hoặc đánh giá các yếu tố thẩm mỹ. Công nghệ này đang ngày càng được sử dụng rộng rãi trong các lĩnh vực bảo mật, thương mại và y tế, giúp cải thiện độ chính xác và hiệu quả trong việc nhận diện và phân tích khuôn mặt người.
- **Mục tiêu và nội dung**
- Chạy được chương trình nhận dạng khuôn mặt (face recognition) để đăng nhập hệ thống
- Chạy được chương trình chấm điểm khuôn mặt (face scoring)
- Tìm hiểu được về Dlib và face-recognition,face-scoring
- Nắm được các giải pháp đã đề ra.
- **Phương thức thực hiện**
- Nghiên cứu công nghệ: Tìm hiểu về Dlib, face-recognition, và các thuật toán chấm điểm khuôn mặt.
- Xây dựng mô hình: Phát triển mô hình nhận diện và chấm điểm khuôn mặt bằng cách sử dụng các thư viện đã nghiên cứu.
- Kiểm thử và tối ưu: Thử nghiệm mô hình với dữ liệu thực tế và tối ưu hóa hiệu suất.
- Triển khai: Đưa hệ thống vào sử dụng và đánh giá kết quả.
# II.Cài Đặt
- Các thư viện cần thiết được ghi lại trong file requirements.txt
- pip install -r requirements.txt
 - **1.Thu thập Dữ liệu**
Yêu cầu về dữ liệu: Cần thu thập ít nhất 1-2 ảnh khuôn mặt rõ ràng của mỗi người, đảm bảo các bộ phận trên khuôn mặt đều hiện diện đầy đủ. Đặt tên cho các tệp ảnh sao cho khớp với tên của người trong ảnh.
Lưu trữ dữ liệu: Lưu các ảnh vào một thư mục,database được sắp xếp rõ ràng.
- **2.Nhận diện Khuôn mặt (Face Recognition)**
Chuẩn bị model: Dlib yêu cầu một số model như facial landmark detector và ResNet model. Bạn có thể tải xuống và giải nén chúng, hoặc sử dụng đoạn mã sau để tải về và giải nén các tệp bắt buộc nếu chúng chưa tồn tại trong thư mục hiện tại.
Load model đã huấn luyện: Sau khi tải xuống, load các mô hình pre-train để sẵn sàng sử dụng.
- **3.Sử dụng thư viện Face-reconition**
-Import thư viện face-reconition và sử dụng các công cụ như detector_backend và model để phát hiện và nhận dạng khuôn mặt.
-face-reconition có nhiều lựa chọn mô hình và metric để đánh giá sự tương đồng, như cosine, euclidean, euclidean_l2.
- **4.Chấm điểm khuôn mặt**
- Sử dụng mô hình phát hiện 68 điểm trên khuôn mặt sau đó tính toán để so sánh độ lệch từ đó đưa ra kết quả
# III.Đặc Trưng
- **Nhận diện khuôn mặt để đăng nhập**
- **Tìm tất cả các khuôn mặt xuất hiện trong một bức ảnh:**
- https://github.com/Software-Engineering-Pka/Face-recog-rating/blob/main/face_rating/stored-faces/z5778559167316_b3a0b36eea0a945a12304b5d6ce84be7.jpg
- https://github.com/Software-Engineering-Pka/Face-recog-rating/blob/main/face_rating/stored-faces/z5778558727844_c8ce578dd20fb48b8f25a82e43e8ce32.jpg
- **Thuật toán:**
- **Truy xuất các khuôn mặt muốn nhận diện trong:**
- https://github.com/Software-Engineering-Pka/Face-recog-rating/tree/main/face_rating/media/images
- sfr = face_recog_model()
- sfr.encoding_faces(os.path.join(settings.MEDIA_ROOT, 'images'))
- **Xác định tọa độ và so sánh khuôn mặt:**
- face_locations, face_names = sfr.comparing_faces(frame)
- **Thêm hình chữ nhật bao quanh khuôn mặt được phát hiện:**
- for face_loc, name in zip(face_locations, face_names):
-   y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
-   cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
-   cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
- **Chấm điểm khuôn mặt**
- Áp dụng tỉ lệ chênh lệch giữa các điểm đối xứng để chấm điểm
