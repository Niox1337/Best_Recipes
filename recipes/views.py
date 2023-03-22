from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import UserProfile, Tag, Review, Rating, Recipe
from recipes.forms import *
from recipes.models_helpers import *

# Create your views here.

def index(request):
    response = render(request, 'recipes/index.html')
    return response


def login(request):
    response = render(request, 'recipes/login.html')
    return response


def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered
    }

    response = render(request, 'recipes/sign_up.html', context=context_dict)
    return response


def about(request):
    response = render(request, 'recipes/about.html')
    return response

def profile(request, user_name_slug):
    user = get_user_by_user_name_slug(user_name_slug)
    context_dict = {
        "user" : user
    }
    response = render(request, "recipes/profile.html", context=context_dict)
    return response