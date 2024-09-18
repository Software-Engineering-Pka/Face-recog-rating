import numpy as np
class ScoreModel:
    def __init__(self,shape):
        self.shape = shape
        self.left_eye = shape[36:42]  
        self.right_eye = shape[42:48]
        self.face_center_point = (self.left_eye[0][0] + self.right_eye[3][0]) // 2
        self.nose_points = shape[27:35] 
        self.mouth_points = shape[48:67]
        self.jawline_points = shape[0:17]
        
    def calculate_face_width(self):
        left_jaw_point = self.jawline_points[0]  
        right_jaw_point = self.jawline_points[-1]  
        
        # Tính độ rộng của khuôn mặt
        face_width = np.linalg.norm(left_jaw_point - right_jaw_point)
        return face_width
    def score_distance(self,points):
        list_points = []
        for i in range(0,len(points)):
            list_points.append(abs(points[i][0] - self.face_center_point))
        mean_score = np.mean(np.abs(np.array(list_points)))
        return mean_score
        
    def score_jawline(self):
        left_distances = []
        right_distances = []
        for i in range(0, len(self.jawline_points)//2):
            left_distances.append(abs(self.jawline_points[i][0] - self.face_center_point))
            right_distances.append(abs(self.jawline_points[-(i+1)][0] - self.face_center_point))
        print(np.abs(np.array(left_distances) - np.array(right_distances)))
        symmetry_score = np.mean(np.abs(np.array(left_distances) - np.array(right_distances)))

        # print(f"Điểm đối xứng đường viền hàm: {symmetry_score:.2f}")

        score = 10 - abs(5-symmetry_score)
        return score
            
    def score_eye(self):
        left_mean_score = self.score_distance(self.left_eye)
        right_mean_score = self.score_distance(self.right_eye)
        delta_mean = abs(left_mean_score-right_mean_score)
        print("Do lech giua 2 mat:",delta_mean)
        if (delta_mean > 1):
            print("2 mắt không đối xứng")
        else:
            print("2 mắt đối xứng")
        score = 9 - 0.5
        return score
    
    def score_mouth(self):
        # Tách các điểm tương ứng cho môi trên và môi dưới
        upper_outer_lip = self.mouth_points[0:7]   
        upper_inner_lip = self.mouth_points[12:16]
        lower_outer_lip = self.mouth_points[6:12]  
        lower_inner_lip = self.mouth_points[16:19] 

        # Tính chiều cao môi trên và môi dưới
        upper_lip_height = np.mean([np.linalg.norm(upper_outer_lip[i] - upper_inner_lip[i]) for i in range(len(upper_inner_lip))])
        lower_lip_height = np.mean([np.linalg.norm(lower_outer_lip[i] - lower_inner_lip[i]) for i in range(len(lower_inner_lip))])
        ratio_height = upper_lip_height / lower_lip_height
        
        # Tính độ rộng môi
        lip_width = np.linalg.norm(self.mouth_points[0] - self.mouth_points[6])  # Khoảng cách giữa điểm 48 và 54

        greate_ratio = 7 / 8
        
        # Tính điểm dựa trên sự khác biệt giữa ratio_height và greate_ratio
        difference = abs(ratio_height - greate_ratio)
        # Chuyển đổi sự khác biệt thành điểm số trên thang 10
        score = max(0, 10 - difference * 20)  # Tùy chỉnh hệ số (20) theo yêu cầu

        # Tổng hợp các điểm đánh giá cho môi
        lip_score = {
            'ratio_height': ratio_height,
            'ratio_width': lip_width / self.calculate_face_width(),
            'score': score
        }
        return score
    def score_nose(self):
            # Đo độ rộng của cánh mũi
            nose_wing_left = np.linalg.norm(self.shape[31] - self.shape[35])  # Khoảng cách giữa các điểm cánh mũi trái và phải
            nose_wing_right = np.linalg.norm(self.shape[32] - self.shape[34])
            nose_width = (nose_wing_left + nose_wing_right) / 2

            # Đo độ rộng của sống mũi
            nose_bridge = np.linalg.norm(self.shape[27] - self.shape[30])  # Khoảng cách giữa điểm 27 và điểm 30
            face_width = self.calculate_face_width()
            greate_score_width = 0.2
            score = ((nose_width/face_width)/greate_score_width)*10
            # nose_score = {
            #     'score':score
            # }
            return score
    def final_result(self):
        score_jawline = self.score_jawline()
        score_eye = self.score_eye()
        score_mouth = self.score_mouth()
        score_nose = self.score_nose()
        
        score_mean = (score_jawline + score_eye + score_mouth + score_nose) / 4 
        return {
            "Jawline":score_jawline,
            "Eye":score_eye,
            "Mouth":score_mouth,
            "Nose":score_nose,
            "Mean":score_mean
        }