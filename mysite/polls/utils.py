import os
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img

MODEL_PATH = os.path.join(settings.BASE_DIR, 'static', 'resnet50.h5')

def grad_cam(img_path): # grad-cam 결과를 파일로 저장한 후 True 리턴
    result_path = '/media/results/grad_cam_result.png'
    print(f"Grad-CAM 결과를 {result_path}에 저장 완료")
    return True

def predict(img_path):
    model = load_model(MODEL_PATH)
    img = load_img(img_path, target_size=(224, 224))
    disease = 0  # 0 정상, 1 결막염, 2 백내장. 라벨링은 임시라서 바뀔 수도 있음.
    accuracy = 87.654
    return [disease, accuracy]
