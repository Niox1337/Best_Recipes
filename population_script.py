import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'Best_Recipes.settings')
from random import randint
from datetime import date

import django
from django.template.defaultfilters import slugify
django.setup()
from recipes.models import UserProfile, Tag, Review, Rating, Recipe
from django.contrib.auth.models import User
from recipes.models_helpers import *

def populate():

    USER_ONE_USERNAME = "UserOne"
    USER_TWO_USERNAME = "UserTwo"
    USER_THREE_USERNAME = "UserThree"
    NEEDS_SLUGGED_USERNAME = "Slug Me Up"

    test_users = [
        {
            "first_name": "User One",
            "last_name": "May",
            "email": "fake@notreal.no",
            "date_of_birth": date.today(),
            "password": "FIXTHIS",
            "user_description": "The first test user",
            "profile_picture": None,
            "user_name": USER_ONE_USERNAME,
        },
        {
            "first_name": "User Two",
            "last_name": "Loan",
            "email": "still@notreal.no",
            "date_of_birth": date.today(),
            "password": "FIXTHIS",
            "user_description": "The second test user",
            "profile_picture": None,
            "user_name": USER_TWO_USERNAME,
        },
        {
            "first_name": "User Three",
            "last_name": "Lewis",
            "email": "veryfake@notreal.no",
            "date_of_birth": date.today(),
            "password": "FIXTHIS",
            "user_description": "The third test user",
            "profile_picture": None,
            "user_name": USER_THREE_USERNAME,
        },
        {
            "first_name": "User Four",
            "last_name": "Lou",
            "email": "veryffffake@notreal.no",
            "date_of_birth": date.today(),
            "password": "FIXTHIS",
            "user_description": "The fourt test user",
            "profile_picture": None,
            "user_name": NEEDS_SLUGGED_USERNAME,
        },
    ]


    for test_user in test_users:
        add_user_profile(test_user)
    
    test_recipe_one = {
        "keys": {
            "creator": USER_ONE_USERNAME,
            "savedBy": [USER_THREE_USERNAME]
        },
        "other": {
        "name": "Chicken Tenders",
        "text": "Crush the rice krispies. Mix the flour and seasonings together. Crush the rice krispies and mix them into the bowl. Roll the chicken tender in the bowl. Cook the chicken tenders then sprinkle on the cheese.",
        "ingredients": "\
30g rice flour\n\
half tsp salt\n\
quater tsp pepper\n\
1 cup gluten free rice krispies\n\
half cup  finely shaved parmesan cheese\n\
half tsp dried thyme\n\
1 egg\n\
800g chicken tenders\n",
    "noOfRatings": 5,
    "recipePicture": None,
    "id": 1,
    "views": 50
    }
    }

    test_recipe_two = {
        "keys": {
            "creator": USER_TWO_USERNAME,
            "savedBy": [USER_ONE_USERNAME]
        },
        "other": {
        "name": "Chinese Noodle Soup",
        "text": "Crush the garlic. Mix the sauces, oil and sugar. Precook the vegetables and chicken. Put all in a pot with the noodles and cook.",
        "ingredients": "\
garlic\n\
soy sauce\n\
sugar\n\
sesame oil\n\
noodles\n\
chicken\n\
vegetables\n\
",
    "noOfRatings": 10,
    "recipePicture": None,
    "id": 2,
    "views": 25
    }
    }

    add_recipe(test_recipe_one)
    add_recipe(test_recipe_two)

    western_tag = {
        "keys" : {
            "recipe_ids" : [test_recipe_one["other"]["id"]]
        },
        "other" : {
            "tag" : Tag.WESTERN_TAG
        }
    }

    asian_tag = {
        "keys" : {
            "recipe_ids" : [test_recipe_two["other"]["id"]]
        },
        "other" : {
            "tag" : Tag.ASIAN_TAG
        }
    }

    indian_tag = {
        "keys" : {
            "recipe_ids" : []
        },
        "other" : {
            "tag" : Tag.INDIAN_TAG
        }
    }

    chinese_tag = {
        "keys" : {
            "recipe_ids" : []
        },
        "other" : {
            "tag" : Tag.CHINESE_TAG
        }
    }

    african_tag = {
        "keys" : {
            "recipe_ids" : []
        },
        "other" : {
            "tag" : Tag.AFRICAN_TAG
        }
    }

    american_tag = {
        "keys" : {
            "recipe_ids" : []
        },
        "other" : {
            "tag" : Tag.AMERICAN_TAG
        }
    }

    other_tag = {
        "keys" : {
            "recipe_ids" : []
        },
        "other" : {
            "tag" : Tag.OTHER_TAG
        }
    }

    # TODO: figure out how to handle tag initlization seperatetly from population script
    add_tag(western_tag)
    add_tag(asian_tag)
    add_tag(indian_tag)
    add_tag(chinese_tag)
    add_tag(african_tag)
    add_tag(american_tag)
    add_tag(other_tag)

    test_recipe_review = {
        "keys": {
            "creator": get_user_by_user_name(USER_THREE_USERNAME),
            "recipe": get_recipe_by_id(test_recipe_two["other"]["id"]),
        },
        "other": {
        "text": "Released a pox into my house and cursed my crops. Needs more salt. One star.",
        "noOfRatings": 5,
        "rating": 1,
        "id": 1
        }
    }

    add_review(test_recipe_review)

    test_recipe_rating = {
        "keys": {
            "creator": get_user_by_user_name(USER_ONE_USERNAME),
            "recipe": get_recipe_by_id(test_recipe_two["other"]["id"]),
            "review": None,
        },
        "other": {
        "recipeOrReview": True,
        "rating": 5,
        "id" : 1,
        },
    }

    test_review_rating = {
        "keys": {
            "creator": get_user_by_user_name(USER_THREE_USERNAME),
            "recipe": None,
            "review": get_review_by_id(test_recipe_review["other"]["id"]),
        },
        "other": {
        "recipeOrReview": False,
        "rating": 1,
        "id" : 2,
        },
    }

    add_rating(test_recipe_rating)
    add_rating(test_review_rating)

    print(calcuate_recipe_rating(get_recipe_by_recipe_name_slug(slugify(test_recipe_two["other"]["name"]))))

def add_user_profile(info_dict):

    user = User.objects.get_or_create(username=info_dict["user_name"])[0]
    # definitely wrong probably
    user.password=info_dict["password"]
    user.email=info_dict["email"]
    
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.last_name=info_dict["last_name"]
    
    profile.date_of_birth=info_dict["date_of_birth"]

    profile.user_description=info_dict["user_description"]
    profile.profile_picture=info_dict["profile_picture"]
    profile.user_name=info_dict["user_name"]
    profile.save()

def add_recipe(info_dict):
    keys = info_dict["keys"]
    other = info_dict["other"]

    creator = get_user_by_user_name(keys["creator"])

    recipe = Recipe.objects.get_or_create(creator=creator, id=other["id"])[0]

    recipe.name = other["name"]
    recipe.text = other["text"]
    recipe.views = other["views"]
    recipe.ingredients = other["ingredients"]
    recipe.no_of_ratings = other["noOfRatings"]
    recipe.recipe_picture = other["recipePicture"]

    recipe.creator = get_user_by_user_name(keys["creator"])
    for saver in keys["savedBy"]:
        # TODO: manytomanyfields are correct in the database but NOT the admin view - do not know why
        recipe.saved_by.add(get_user_by_user_name(saver))

    recipe.save()

def add_tag(info_dict):
    keys = info_dict["keys"]
    other = info_dict["other"]
    tag = Tag.objects.get_or_create(tag=other["tag"])[0]

    # TODO: manytomanyfields are correct in the database but NOT the admin view - do not know why
    for recipe_id in keys["recipe_ids"]:
        tag.recipe.add(get_recipe_by_id(recipe_id))

    tag.save()

def add_review(info_dict):
    keys = info_dict["keys"]
    other = info_dict["other"]

    review = Review.objects.get_or_create(creator=keys["creator"], recipe=keys["recipe"], id=other["id"])[0]
    review.creator = keys["creator"]
    review.recipe = keys["recipe"]
    # TODO: update admin models so to make the name of text display properly
    review.text = other["text"]
    review.no_of_ratings = other["noOfRatings"]
    review.review_rating = other["rating"]

    review.save()

def add_rating(info_dict):
    keys = info_dict["keys"]
    other = info_dict["other"]

    rating = Rating.objects.get_or_create(creator=keys["creator"], recipe=keys["recipe"], review=keys["review"], id=other["id"])[0]

    rating.creator = keys["creator"]
    rating.recipe = keys["recipe"]
    rating.review = keys["review"]
    rating.recipe_or_review = other["recipeOrReview"]
    rating.rating = other["rating"]
    
    rating.save()

if __name__ == '__main__':
    print('Starting recipes population script...')
    populate()