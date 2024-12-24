from django.shortcuts import render
from django.http import HttpResponse
from .dash_app import dash_app

# Create your views here.

def dash_view(request):
    return HttpResponse(dash_app.index(), content_type='text/html')