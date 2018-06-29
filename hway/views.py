
from django.shortcuts import  render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


import requests
import json

def home(request):
    return HttpResponse("HackerRank Web")