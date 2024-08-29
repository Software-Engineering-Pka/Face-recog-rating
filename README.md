# Face-recognition
**I.Giới Thiệu về dự án**
- Face-recognition là công nghệ nhận diện khuôn mặt dựa trên các đặc điểm sinh trắc học. Công nghệ này sử dụng các thuật toán để phân tích các đặc trưng trên khuôn mặt, như khoảng cách giữa mắt, hình dáng mũi, và cấu trúc xương hàm, từ đó xác định danh tính của người dùng. Chấm điểm khuôn mặt là quá trình đánh giá và cho điểm các đặc điểm khuôn mặt dựa trên các tiêu chí thẩm mỹ hoặc sinh trắc học. Điểm số này có thể được sử dụng trong nhiều ứng dụng, từ xác thực danh tính đến phân tích tâm lý học hành vi hoặc đánh giá các yếu tố thẩm mỹ. Công nghệ này đang ngày càng được sử dụng rộng rãi trong các lĩnh vực bảo mật, thương mại và y tế, giúp cải thiện độ chính xác và hiệu quả trong việc nhận diện và phân tích khuôn mặt người.
**Mục tiêu và nội dung**
- Chạy được chương trình nhận dạng khuôn mặt (face recognition)
- Tìm hiểu được về Dlib và face detection
- Nắm được các giải pháp đã đề ra.
**Phương thức thực hiện**
- Dlib + Euclipse (hay còn được gọi là KNN)
- Dlib + SVM
**II.Cài Đặt**
-Cài đặt Cmake: Mở terminal và nhập lệnh sau để cài đặt Cmake:pip install cmake
-Cài đặt Dlib: Tiếp theo, cài đặt thư viện Dlib bằng lệnh:pip install dlib
 1.Thu thập Dữ liệu
Yêu cầu về dữ liệu: Cần thu thập ít nhất 1 2 ảnh khuôn mặt rõ ràng của mỗi người, đảm bảo các bộ phận trên khuôn mặt đều hiện diện đầy đủ. Đặt tên cho các tệp ảnh sao cho khớp với tên của người trong ảnh.
Lưu trữ dữ liệu: Lưu các ảnh vào một thư mục được sắp xếp rõ ràng.
 2.Nhận diện Khuôn mặt (Face Detection)
Chuẩn bị model: Dlib yêu cầu một số model như facial landmark detector và ResNet model. Bạn có thể tải xuống và giải nén chúng, hoặc sử dụng đoạn mã sau để tải về và giải nén các tệp bắt buộc nếu chúng chưa tồn tại trong thư mục hiện tại.
Load model đã huấn luyện: Sau khi tải xuống, load các mô hình pre-train để sẵn sàng sử dụng.
**Phương pháp 1**: Sử dụng khoảng cách Euclidean
Đọc các file npz đã được tạo từ dữ liệu tập huấn luyện (train data), chuyển ảnh mới thành vector và tính toán khoảng cách Euclidean để xác định danh tính.
**Phương pháp 2**: Sử dụng SVM
Import mô hình SVM từ thư viện sklearn và áp dụng nó lên dữ liệu trong file npz đã tạo, sau đó so sánh để đưa ra kết quả nhận dạng.
3.Sử dụng DeepFace
-Import thư viện DeepFace và sử dụng các công cụ như detector_backend và model để phát hiện và nhận dạng khuôn mặt.
-DeepFace có nhiều lựa chọn mô hình và metric để đánh giá sự tương đồng, như cosine, euclidean, euclidean_l2.
**III.Đặc Trưng**
- **Tìm tất cả các khuôn mặt xuất hiện trong một bức ảnh:**
- https://github.com/Software-Engineering-Pka/Face-recog-rating/blob/main/face_rating/stored-faces/z5778559167316_b3a0b36eea0a945a12304b5d6ce84be7.jpg
- https://github.com/Software-Engineering-Pka/Face-recog-rating/blob/main/face_rating/stored-faces/z5778558727844_c8ce578dd20fb48b8f25a82e43e8ce32.jpg
- **Thuật toán:**
- **Truy xuất các khuôn mặt muốn nhận diện trong:** -https://github.com/Software-Engineering-Pka/Face-recog-rating/tree/main/face_rating/media/images
- sfr = face_recog_model()
- sfr.encoding_faces(os.path.join(settings.MEDIA_ROOT, 'images'))
- **Xác định tọa độ và so sánh khuôn mặt:**
- face_locations, face_names = sfr.comparing_faces(frame)
- **Thêm hình chữ nhật bao quanh khuôn mặt được phát hiện:**
- for face_loc, name in zip(face_locations, face_names):
-   y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
-   cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
-   cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
