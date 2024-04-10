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
        form = ProductForm(request.POST, request.FILES) # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
        if form.is_valid():
            product = form.save()
            img_path = product.imgfile.path
            if grad_cam(img_path): # grad-cam 시행 후 이미지 파일 저장.
                print('Complete grad_cam')
            disease, accuracy = predict(img_path)  # 모델을 통해 예측 시행 후 disease에 값 넣기. 0 정상, 1 결막염, 2 백내장. 라벨링은 임시라서 바뀔 수도 있음.
            return render(request, "index.html", {'product': product, 'form': ProductForm(), 'disease': disease, 'accuracy': accuracy})
            # form.save()
            # products = Product.objects.all() # 모든 Product 인스턴스를 불러옵니다.
            # return render(request, "index.html", {'products': products})
    return redirect('index') # request.method 가 'GET'이거나 invalid 경우
