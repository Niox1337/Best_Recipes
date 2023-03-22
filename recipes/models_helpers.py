import django
from recipes.models import UserProfile, Tag, Review, Rating, Recipe

def get_user_by_user_name(user_name):
    users = UserProfile.objects.all().filter(user_name=user_name)
    if (len(users)) == 0:
        raise Exception("Could not find user " + user_name)
    elif (len(users) > 1):
        raise Exception("More than one user with usermame " + user_name)
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
    
def get_review_by_id(id):
    reviews = Review.objects.all().filter(id=id)
    if (len(reviews)) == 0:
        raise Exception("Could not find review with id " + str(id))
    elif (len(reviews) > 1):
        raise Exception("More than one review with id " + str(id))
    else:
        return reviews[0]