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


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("recipes:index"))
            else:
                return HttpResponse("Your account is currently on hold \nPlease contact admins")
        else:
            return HttpResponse("Invalid username or password")
    else:
        return render(request, 'recipes/login.html')

def user_logout(request):
    logout(request)
    return render(request, 'recipes/index.html')

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
            if 'picture' in request.FILES:
                profile.profile_picture = request.FILES['picture']
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

@login_required
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
        "edit_recipe_form": edit_recipe_form,
        "tags": Tag.objects.all()
    }

    response = render(request, 'recipes/edit_recipe.html', context=context_dict)
    return response

@login_required
def new_recipe(request, user_name_slug):
    if request.method == 'POST':

        user = get_user_by_user_name_slug(user_name_slug)

        print(request.POST)

        edit_recipe_form = EditRecipeForm(request.POST)

        if edit_recipe_form.is_valid():
            creator = user

            recipe = Recipe()

            recipe.creator = creator
            recipe.name = request.POST["name"]
            recipe.text = request.POST["text"]
            recipe.views = 0
            recipe.ingredients = request.POST["ingredients"]
            recipe.no_of_ratings = 0      
            # TODO: TAGS      

            recipe.save()
        else:
            print(edit_recipe_form.errors)

    else:
        edit_recipe_form = EditRecipeForm()

    context_dict = {
        "edit_recipe_form": edit_recipe_form,
        "tags": Tag.objects.all()
    }

    response = render(request, 'recipes/new_recipe.html', context=context_dict)
    return response

def show_recipe(request, recipe_name_slug):
    # TODO: handle non-existent recipe name slugs
    recipe = get_recipe_by_recipe_name_slug(recipe_name_slug)
    context_dict = {
        "recipe" : recipe
    }

    # TODO: updates on every refresh - not ideal but not the biggest problem in the world either
    recipe.views += 1
    recipe.save()

    response = render(request, "recipes/show_recipe.html", context=context_dict)
    return response


def about(request):
    response = render(request, 'recipes/about.html')
    return response


def profile(request, user_name_slug):
    user_name_slug = slugify(user_name_slug)
    user = get_user_by_user_name_slug(user_name_slug)

    recipes = Recipe.objects.filter(creator=user)

    context_dict = {
        "user" : user,
        "recipes": recipes
    }

    response = render(request, "recipes/profile.html", context=context_dict)
    return response

def favourites(request, user_name_slug):
    # technically user.username could be passed in over a proper slug so we double slug just in case
    user_name_slug = slugify(user_name_slug)
    user = get_user_by_user_name_slug(user_name_slug)

    saved_recipes = Recipe.objects.filter(saved_by=user)

    context_dict = {
        "user" : user,
        "saved_recipes": saved_recipes
    }


    response = render(request, "recipes/favourites.html", context=context_dict)
    return response