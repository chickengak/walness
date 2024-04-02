from django.shortcuts import render, redirect           # response의 응답페이지 함수
from django.http import HttpResponse, JsonResponse      # 응답페이지의 형식
from django.conf import settings
from django.contrib import messages
# from .utils import *


# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")

def left_sidebar_view(request):
    return render(request, "left-sidebar.html")

def right_sidebar_view(request):
    return render(request, "right-sidebar.html")

def no_sidebar_view(request):
    context = {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, "no-sidebar.html", context)
