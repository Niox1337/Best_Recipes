from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import UserProfile, Tag, Review, Rating, Recipe

# Create your views here.

def index(request):
    response = render(request, 'recipes/index.html')
    return response

def login(request):
    response = render(request, 'recipes/login.html')
    return response

def sign_up(request):
    response = render(request, 'recipes/sign_up.html')
    return response

def about(request):
    response = render(request, 'recipes/about.html')
    return response