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