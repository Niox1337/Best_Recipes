from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Category, Page
from recipes.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Create your views here.


