import os
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img
import cv2
import numpy as np

MODEL_PATH = os.path.join(settings.BASE_DIR, 'static', 'resnet50.h5')


def grad_cam(img_path):
    model = ResNet50(weights='imagenet', include_top=True)

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)

    last_conv_layer_name = "conv5_block3_out"
    last_conv_layer = model.get_layer(last_conv_layer_name)
    model = tf.keras.models.Model(model.inputs, [model.output, last_conv_layer.output])

    with tf.GradientTape() as tape:
        model_out, last_conv_layer = model(img_array)
        class_out = model_out[:, np.argmax(model_out[0])]
        grads = tape.gradient(class_out, last_conv_layer)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = last_conv_layer[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        heatmap /= tf.reduce_max(heatmap)

    heatmap = heatmap.numpy()

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    gradcam_on_image = cv2.addWeighted(img, 0.8, heatmap, 0.2, 0)

    result_path = os.path.join(settings.MEDIA_ROOT, 'results', 'grad_cam_result.png')
    cv2.imwrite(result_path, gradcam_on_image)

    return result_path

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
