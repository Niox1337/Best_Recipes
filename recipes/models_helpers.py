import django
from recipes.models import UserProfile, Tag, Review, Rating, Recipe
from django.template.defaultfilters import slugify

def get_user_by_user_name(user_name):
    return get_user_by_user_name_slug(slugify(user_name))
    
def get_user_by_user_name_slug(user_name_slug):
    users = UserProfile.objects.all().filter(user_name_slug=user_name_slug)
    if (len(users)) == 0:
        raise Exception("Could not find user with user name slug " + user_name_slug)
    elif (len(users) > 1):
        raise Exception("More than one user with user name slug e " + user_name_slug)
    else:
        return users[0]

def get_user_by_user_name_slug(user_name_slug):
    users = UserProfile.objects.all().filter(user_name_slug=user_name_slug)
    if (len(users)) == 0:
        raise Exception("Could not find user with user name slug " + user_name_slug)
    elif (len(users) > 1):
        raise Exception("More than one user with user name slug e " + user_name_slug)
    else:
        return users[0]

def get_recipe_by_id(id):
    recipes = Recipe.objects.all().filter(id=id)
    if (len(recipes)) == 0:
        raise Exception("Could not find recipe with id " + str(id))
    elif (len(recipes) > 1):
        raise Exception("More than one recipe with id " + str(id))
    else:
        return recipes[0]
    
def get_recipe_by_recipe_name_slug(recipe_name_slug):
    recipes = Recipe.objects.all().filter(recipe_name_slug=recipe_name_slug)
    if (len(recipes)) == 0:
        raise Exception("Could not find recipe with recipe name slug " + recipe_name_slug)
    elif (len(recipes) > 1):
        raise Exception("More than one recipe with recipe name slug " + recipe_name_slug)
    else:
        return recipes[0]
    
def get_review_by_id(id):
    reviews = Review.objects.all().filter(id=id)
    if (len(reviews)) == 0:
        raise Exception("Could not find review with id " + str(id))
    elif (len(reviews) > 1):
        raise Exception("More than one review with id " + str(id))
    else:
        return reviews[0]