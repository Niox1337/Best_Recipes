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
    if request.method == 'POST':
        sign_up_form = RegisterForm(request.POST)
        
        if sign_up_form.is_valid():
            sign_up_form.save()
        else:
            print(sign_up_form.errors)

    else:
        sign_up_form = RegisterForm()
        

    context_dict = {
        "sign_up_form" : sign_up_form
    }

    response = render(request, 'recipes/sign_up.html', context=context_dict)
    return response

def edit_recipe(request):
    
    if request.method == 'POST':

        print(request.POST)

        edit_recipe_form = EditRecipeForm(request.POST)
        
        if edit_recipe_form.is_valid():
            edit_recipe_form.save()
        else:
            print(edit_recipe_form.errors)

    else:
        edit_recipe_form = EditRecipeForm()
        

    context_dict = {
        "edit_recipe_form" : edit_recipe_form,
        "tags": Tag.objects.all()
    }

    response = render(request, 'recipes/edit_recipe.html', context=context_dict)
    return response

def profile(request, user_name_slug):
    # TODO: handle non-existent user name slugs
    user = get_user_by_user_name_slug(user_name_slug)
    context_dict = {
        "user" : user
    }
    response = render(request, "recipes/profile.html", context=context_dict)
    return response

def show_recipe(request, recipe_name_slug):
    # TODO: handle non-existent recipe name slugs
    recipe = get_recipe_by_recipe_name_slug(recipe_name_slug)
    context_dict = {
        "recipe" : recipe
    }
    response = render(request, "recipes/show_recipe.html", context=context_dict)
    return response

def about(request):
    response = render(request, 'recipes/about.html')
    return response