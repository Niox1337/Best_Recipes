from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
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
        profile_form = UserProfileForm(request.POST, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid():
            # User form
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # UserProfile form
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.profile_picture = request.FILES['picture']

            profile.save()
            registered = True
            """
            user = authenticate(username=request.POST.get("username"),
                                password=request.POST.get("password"))
            login(request, user)
            """
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

def give_rating(request):
    if request.is_ajax and request.method == "GET":
        given_rating = request.GET.get("rating", None)
        user = request.GET.get("user", None)
        recipe_name_slug = request.GET.get("recipe", None)

        creator = get_user_by_user_name_slug(slugify(user))
        reicpe = get_recipe_by_recipe_name_slug(recipe_name_slug)
        
        rating = Rating.objects.get_or_create(creator=creator, recipe=reicpe, recipe_or_review=True)[0]
        rating.rating = int(given_rating)
        rating.save()

    return JsonResponse({}, status = 200)

def get_rating(request):
    if request.is_ajax and request.method == "GET":
        user = request.GET.get("user", None)
        recipe_name_slug = request.GET.get("recipe", None)

        creator = get_user_by_user_name_slug(slugify(user))
        reicpe = get_recipe_by_recipe_name_slug(recipe_name_slug)
        
        rating = Rating.objects.get_or_create(creator=creator, recipe=reicpe, recipe_or_review=True)[0]

    return JsonResponse({"rating": rating.rating}, status = 200)

@login_required
def edit_recipe(request, recipe_name_slug):
    
    recipe_found = False
    found_recipe = None

    # because creator id is mandatory and we don't have it we need to do this
    for recipe in Recipe.objects.all():
        print("checking:" + recipe.recipe_name_slug)
        if recipe.recipe_name_slug == recipe_name_slug:
            found_recipe = recipe
            recipe_found = True
    
    if not recipe_found:
        raise Exception("Recipe with recipe name slug " + recipe_name_slug + " not found")

    recipe_creator = recipe.creator.user_name_slug

    if request.method == 'POST':

        #found_recipe.delete()

        print(request.POST)

        edit_recipe_form = EditRecipeForm(request.POST)

        if edit_recipe_form.is_valid():
            edit_recipe_form.save()
        else:
            print(edit_recipe_form.errors)

    else:
        initial_values = {
            "name": recipe.name,
            "text": recipe.text,
            "ingredients": recipe.ingredients,

        }
        edit_recipe_form = EditRecipeForm(initial={'text': "HI MAW", 'western': 'on'})

    context_dict = {
        "edit_recipe_form": edit_recipe_form,
        "tags": Tag.objects.all(),
        "recipe_creator": recipe_creator,
    }

    response = render(request, 'recipes/edit_recipe.html', context=context_dict)
    return response


@login_required
def delete_recipe(request, recipe_name_slug):
    recipe = get_recipe_by_recipe_name_slug(recipe_name_slug)

    context_dict = {
        "recipe" : recipe,
    }

    response = render(request, "recipes/delete_recipe.html", context=context_dict)
    return response

@login_required
def true_delete_recipe(request, recipe_name_slug):
    recipe = get_recipe_by_recipe_name_slug(recipe_name_slug)
    recipe_name = recipe.name

    recipe.delete()

    context_dict = {
        "recipe_name" : recipe_name,
    }

    return render(request, 'recipes/index.html')
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
            recipe.save()

            for tag in Tag.objects.all():
                lowered_name = tag.tag.lower()
                if lowered_name in request.POST:
                    tag.recipe.add(recipe)
                tag.save()

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



def show_tag(request, tag_name_slug):
    # TODO: consder making recipes None by default and making list when tag found so we can do {% if recipes %} later on
    recipes = []
    tag_found = False
    found_tag = None

    for tag in Tag.objects.all():
        if tag_name_slug == slugify(tag.tag):
            tag_found = True
            found_tag = tag
            recipes_in_tag = tag.recipe.all()
            for recipe in recipes_in_tag:
                recipes.append(recipe)
    if not tag_found:
        raise Exception("Tag " + tag_name_slug + " not found")

    if (len(recipes) == 0):
        recipes = None

    context_dict = {
        "tag": found_tag,
        "recipes": recipes
    }

    response = render(request, 'recipes/show_tag.html', context=context_dict)
    return response


def show_recipe(request, recipe_name_slug):
    # TODO: handle non-existent recipe name slugs
    recipe = get_recipe_by_recipe_name_slug(recipe_name_slug)

    class TagMeta:
        def __init__(self, tag, tag_name_slug):
            self.tag = tag
            self.tag_name_slug = tag_name_slug

    tag_metas = []

    for tag in Tag.objects.all():
        recipes_in_tag = tag.recipe.all()
        if recipe in recipes_in_tag:
            tag_meta = TagMeta(tag.tag, slugify(tag.tag))
            tag_metas.append(tag_meta)

    if (len(tag_metas)) == 0:
        tag_metas = None

    context_dict = {
        "recipe": recipe,
        "tag_metas": tag_metas,
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
        "user": user,
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
        "user": user,
        "saved_recipes": saved_recipes
    }

    response = render(request, "recipes/favourites.html", context=context_dict)
    return response
