import face_recognition
import cv2
import os
import glob
import numpy as np

class face_recog_model:
    def __init__(self):
        self.existed_face_encodings = []
        self.exised_face_names = []
        
    def encoding_faces(self,images_folder_address):
        images_path = glob.glob(os.path.join(images_folder_address, "*.*"))
        print(f"Found {len(images_path)}")
        for image_path in images_path:
            img = cv2.imread(image_path)
            rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
            basename = os.path.basename(image_path)
            (name,ext) = os.path.splitext(basename)
            self.existed_face_encodings.append(img_encoding)
            self.exised_face_names.append(name)
        print("Encodings done!")
            
    def comparing_faces(self,frame):
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