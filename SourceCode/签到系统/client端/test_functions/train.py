# 第二步：训练模型

# 1. 导入第三方库
import cv2
import os
from PIL import Image
import numpy as np

# 2. 加载特征提取模型

recognizer_create = cv2.face.LBPHFaceRecognizer_create()

# 3. 数据处理
def data_translate(path):
    face_data = []
    id_data = []
    file_list = [os.path.join(path, f) for f in os.listdir(path)]
    # print(file_list)
    for file in file_list:
        PIL_image = Image.open(file).convert("L")
        np_image = np.array(PIL_image, 'uint8')
        image_id = int(file.split('.')[1])
        # print(image_id)
        face_data.append(np_image)
        id_data.append(image_id)
    return face_data, id_data

# 4. 训练模型
Face, ID = data_translate('dataset')
recognizer_create.train(Face, np.array(ID))
print('训练完成')

# 5. 保存模型
recognizer_create.save('face_model.yml')
print('模型已保存')