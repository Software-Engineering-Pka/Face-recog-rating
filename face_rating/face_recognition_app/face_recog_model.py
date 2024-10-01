import face_recognition
import cv2
import os
import glob
import numpy as np
from account.models import AccountModel
import json
class face_recog_model:
    def __init__(self):
        self.existed_face_encodings = []
        self.exised_face_names = []
        # self.frame_resizing = 0.25

    def encoding_faces(self):
        accounts = AccountModel.objects.all()
        for account in accounts:
            self.exised_face_names.append(account.username)
            print(account.face_image_encoding)
            if account.face_image_encoding:
                encoding = np.array(json.loads(account.face_image_encoding))
                self.existed_face_encodings.append(encoding)
        # images_path = glob.glob(os.path.join(images_folder_address, "*.*"))
        # print(f"Found {len(images_path)}")
        # for image_path in images_path:
        #     img = cv2.imread(image_path)
        #     rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #     img_encoding = face_recognition.face_encodings(rgb_img)[0]
        #     basename = os.path.basename(image_path)
        #     (name,ext) = os.path.splitext(basename)
        #     self.existed_face_encodings.append(img_encoding)
            
        #     self.exised_face_names.append(name)
        # print("Encodings done!")
        # print(self.existed_face_encodings)
            
    def comparing_faces(self,frame):
        # small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        names = []        

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.existed_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.existed_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.exised_face_names[best_match_index]
            names.append(name)

        face_locations = np.array(face_locations)
        return face_locations.astype(int), names