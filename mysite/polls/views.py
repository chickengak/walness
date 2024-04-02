from django.shortcuts import render, redirect           # response의 응답페이지 함수
from django.http import HttpResponse, JsonResponse      # 응답페이지의 형식
from django.conf import settings
from django.contrib import messages
import googlemaps
import requests
import json
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
    headers = {'Content-Type': 'application/json',}
    params = {'key': settings.GOOGLE_MAPS_API_KEY,}
    json_data = {
        'homeMobileCountryCode': 310,
        'homeMobileNetworkCode': 410,
        'radioType': 'gsm',
        'carrier': 'Vodafone',
        'considerIp': True,
    }

    response = requests.post('https://www.googleapis.com/geolocation/v1/geolocate', params=params, headers=headers, json=json_data)
    gmaps = googlemaps.Client(key= settings.GOOGLE_MAPS_API_KEY)
    print('---------------------', response.json())
    results = gmaps.places(query="animal hospital", location=(response.json()["location"]["lat"], response.json()["location"]["lng"]), radius=5000)
    print('---------------------', type(results), sep='\n')

    # file_path = 'temp.json'
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(results, file)
    
    context = {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, "no-sidebar.html", context)
