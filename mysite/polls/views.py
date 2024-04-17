from django.shortcuts import render, redirect           # response의 응답페이지 함수
from django.http import HttpResponse, JsonResponse      # 응답페이지의 형식
from django.conf import settings
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .utils import grad_cam, predict
import os
import requests
import json
# from .utils import *


# Create your views here.
def index(request):
    #return render(request, "index.html")
    form = ProductForm() # 초기 폼을 index 페이지에 전달
    return render(request, "index.html", {'form': form})


def left_sidebar_view(request):
    return render(request, "left-sidebar.html")

def right_sidebar_view(request):
    return render(request, "right-sidebar.html")

def no_sidebar_view(request):
    context = {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, "no-sidebar.html", context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            img_path = product.imgfile.path
            gradcam_image_path = grad_cam(img_path)  # grad-cam 이미지 생성
            if gradcam_image_path:  # grad-cam 이미지가 성공적으로 생성되었을 때
                print('Complete grad_cam')
                # predict 함수 호출하여 결과 얻기
                pet_type = request.POST['pet_type']
                print(pet_type)
                disease, accuracy = predict(img_path, pet_type)
                return render(request, "index.html", {'product': product, 'form': ProductForm(), 'gradcam_image_path': gradcam_image_path, 'disease': disease, 'accuracy': accuracy, 'pet_type': pet_type})
            else:  # grad-cam 이미지 생성 실패 시
                messages.error(request, 'Failed to generate Grad-CAM image.')
    return redirect('index')
