# Import the necessary packages
from imutils import face_utils
import dlib
import cv2

# Load the pre-trained model for face landmarks
p = "../algorithm_files/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# Load the image and convert it to grayscale
image = cv2.imread("./Ryan Reynolds.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the grayscale image
rects = detector(gray, 0)

# Loop over the face detections
for (i, rect) in enumerate(rects):
    # Get the facial landmarks
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # Loop over the (x, y) coordinates for the facial landmarks and draw them on the image
    for (x, y) in shape:
        cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

# Display the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
