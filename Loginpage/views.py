from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm

# Create your views here.

def sign_in(request):
     return HttpResponse('Hello World!')
