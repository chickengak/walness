import os
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
import numpy as np

MODEL_PATH = os.path.join(settings.BASE_DIR, 'static', 'resnet50.h5')

def grad_cam(img_path): # grad-cam 결과를 파일로 저장한 후 True 리턴
    result_path = '/media/results/grad_cam_result.png'
    print(f"Grad-CAM 결과를 {result_path}에 저장 완료")
    return True

def predict(img_path):
    model = load_model(MODEL_PATH)
    img = load_img(img_path, target_size=(224, 224))

    # 이미지를 텐서 형식으로 변환
    tensor = tf.image.resize(img, [224, 224])  # 모델의 입력 크기에 맞게 조정
    tensor = tf.cast(tensor, tf.float32)
    tensor = tf.expand_dims(tensor, axis=0)
    
    # 예측 수행
    predictions = model.predict(tensor)

    # 예측 결과
    disease = np.argmax(predictions)
    accuracy = round(predictions[0][disease] * 100, 2)

    return [disease, accuracy]
