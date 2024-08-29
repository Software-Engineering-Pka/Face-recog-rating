import cv2
from imgbeddings import imgbeddings
import os
from PIL import Image
import json
from datetime import datetime




file_name = "./Nguyet.jpg"
def face_detector(file_name):
    alg = "./haarcascade_frontalface_default.xml"

    if not os.path.exists('./stored-faces/'):
        os.makedirs('./stored-faces/')

    haar_cascade = cv2.CascadeClassifier(alg)

    img = cv2.imread(file_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    faces = haar_cascade.detectMultiScale(
        gray_img, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100)
    )

    embedder = imgbeddings()

    embeddings = []
    i = 0

    for x, y, w, h in faces:
        cropped_image = img[y: y + h, x: x + w]
        current_time = datetime.now()

        time_str = current_time.strftime("Userid_%Y%m%d_%H%M%S")
        target_file_name = './stored-faces/' + str(time_str) + '.jpg'
        
        cv2.imwrite(target_file_name, cropped_image)
        
        cropped_pil = Image.open(target_file_name)
        
        # embedding = embedder.to_embeddings(cropped_pil)  # Sử dụng embed()
        
        # embedding_list = embedding.tolist()  # Nếu embedding là numpy array
        
        # entry = {
        #     'filename': target_file_name,
        #     'embedding': embedding_list
        # }
        # embeddings.append(entry)
        # i += 1
    # return embeddings

face_detector(file_name)
