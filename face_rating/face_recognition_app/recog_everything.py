import dlib
import cv2

# Đường dẫn đến mô hình định vị khuôn mặt
predictor_path = "shape_predictor_68_face_landmarks.dat"

# Tải mô hình
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Đọc hình ảnh
img = cv2.imread("your_image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Phát hiện khuôn mặt
faces = detector(gray)

for face in faces:
    landmarks = predictor(gray, face)
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

cv2.imshow("Landmarks", img)
cv2.waitKey(0)
