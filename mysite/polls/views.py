from django.shortcuts import render, redirect           # response의 응답페이지 함수
from django.http import HttpResponse, JsonResponse      # 응답페이지의 형식
from django.conf import settings
from django.contrib import messages
from .forms import ProductForm
from .models import Product
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
            return render(request, "index.html", {'product': product, 'form': ProductForm()})
            # form.save()
            # products = Product.objects.all() # 모든 Product 인스턴스를 불러옵니다.
            # return render(request, "index.html", {'products': products})
    else:
        form = ProductForm() # request.method 가 'GET'인 경우
    context = {'form':form}
    return render(request, 'index', context)
