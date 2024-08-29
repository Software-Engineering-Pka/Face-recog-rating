import numpy as np
import json
import face_recognition

# Tải embeddings từ hình ảnh mới

new_image = face_recognition.load_image_file("./gounyung.jpg")
new_embeddings = face_recognition.face_encodings(new_image)

# Danh sách để lưu khoảng cách
list_delta = []

# Đọc dữ liệu từ tệp JSON
with open("./embeddings.json", "r") as file:
    data = json.load(file)

# Chuyển đổi dữ liệu JSON thành mảng NumPy
# Giả sử `data` chứa một danh sách các đối tượng với thuộc tính `embedding`
data_embeddings = [np.array(embed["embedding"]) for embed in data]

# Tính toán khoảng cách Euclidean
for embed_input in new_embeddings:
    for embed_existed in data_embeddings:
        delta_embed = np.linalg.norm(embed_input - embed_existed)
        list_delta.append(delta_embed)

print("List of Euclidean distances:", list_delta)
