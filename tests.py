import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'Best_Recipes.settings')
import django
django.setup()
from django.test import TestCase, Client
from datetime import date
from django.urls import reverse
from recipes.models import UserProfile, Recipe, Review, Rating
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from recipes.models_helpers import *
from population_script import *

USER_ONE_USERNAME = "UserOne"
USER_TWO_USERNAME = "UserTwo"
USER_THREE_USERNAME = "UserThree"
NEEDS_SLUGGED_USERNAME = "Slug Me Up"

class SignUpTest(TestCase):

    def set_up(self):
       self.info_dict={
            "first_name":"testFirstName",
            "last_name":"testLastName",
            "email":"testEmail",
            "date_of_birth":date.today(),
            "password":"testpassword",
            "user_description":"testUserDescription",
            "profile_picture":"testProfilePicture",
            "user_name":"testuser",
            }

    def test_add_user(self):
        user_name_slug = slugify(self.info_dict["user_name"])
        add_user_profile(self.info_dict)
        self.assertEqual(get_user_by_user_name_slug(user_name_slug).user_name_slug, user_name_slug)

    def test_max_lengths(self):
        self.user = get_user_by_user_name_slug(slugify(self.info_dict["user_name"]))
        self.assertEqual(
            self.user._meta.get_field('first_name').max_length, 
            UserProfile.FIRST_NAME_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('last_name').max_length, 
            UserProfile.LAST_NAME_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('user_description').max_length, 
            UserProfile.USER_DESCRIPTION_LEN
        )

    def test_delete_user(self):
        user_name_slug = slugify(self.info_dict["user_name"])
        user = get_user_by_user_name_slug(user_name_slug)
        user.delete()
        self.assertEqual(user in UserProfile.objects.all(), False)


class RatingsTest(TestCase):
    def set_up(self):

        self.rating_id = -60
        self.info_dict = {
        "keys": {
            "creator": get_user_by_user_name(USER_ONE_USERNAME),
            "recipe": None,
            "review": None,
        },
        "other": {
        "recipeOrReview": True,
        "rating": 5,
        "id" : self.rating_id,
        },
    }
        self.recipe = Recipe()
        self.recipe.name = "tesyyytttu"
        self.recipe.text = "test"
        self.recipe.creator = get_user_by_user_name(USER_ONE_USERNAME)
        self.info_dict["keys"]["recipe"] = self.recipe
        self.recipe.save()

    def test_ensure_ratings_are_positive(self):
        add_rating(self.info_dict)
        rating = None
        for to_check in Rating.objects.all():
            if to_check.id == self.rating_id:
                rating = to_check
                break
        rating_rating = rating.rating
        self.recipe.delete()
        rating.delete()
        self.assertEquals(rating_rating >= 0, True)



class IndexAndAboutTestCase(TestCase):
    def set_up(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code,200) 


class RecipeViewsTestCase(TestCase):
    def set_up(self):
        self.info_dict = {
            "first_name":"testFirstName",
            "last_name":"testLastName",
            "email":"testEmail",
            "date_of_birth":date.today(),
            "password":"testpassword",
            "user_description":"testUserDescription",
            "profile_picture":"testProfilePicture",
            "user_name":"testuser",
            }
               
        self.client = Client()
        add_user_profile(self.info_dict)
        self.user_name_slug = slugify(self.info_dict["user_name"])
        self.user = get_user_by_user_name_slug(self.user_name_slug)
        
    def test_add_recipe(self):
        self.recipe = Recipe.objects.create(creator=self.user, name='Test Recipe 2', text='This is a test recipe.', views=0, ingredients='Test Ingredient 1, Test Ingredient 2', no_of_ratings=0)
        self.recipe.save()
        self.assertEqual(self.recipe in Recipe.objects.all(), True)

    def test_delete_recipe(self):
        self.recipe.delete()
        self.assertEqual(self.recipe in Recipe.objects.all(), False)

class ProfileAndFavouritesTestCase(TestCase):
    def set_up(self):
        self.user = User.objects.get_or_create(username='testuser')[0]
        self.user.set_password("testpass")
        self.user_profile = UserProfile.objects.get_or_create(user=self.user,user_name_slug=slugify(self.user.username))
        self.url = reverse('profile', kwargs={'user_name_slug': slugify(self.user.username)})
        self.url = reverse('favourites', kwargs={'user_name_slug': slugify(self.user.username)})

        self.client = Client()

    def testprofile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def testfavourites(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

sign_up_test = SignUpTest()
sign_up_test.set_up()
sign_up_test.test_add_user()
sign_up_test.test_max_lengths()
sign_up_test.test_delete_user()

index_and_about_test_case = IndexAndAboutTestCase()
index_and_about_test_case.set_up()
index_and_about_test_case.test_index()
index_and_about_test_case.test_about()

recipe_views_test_case = RecipeViewsTestCase()
recipe_views_test_case.set_up()
recipe_views_test_case.test_add_recipe()
recipe_views_test_case.test_delete_recipe()

profile_and_favourite_test = ProfileAndFavouritesTestCase()
profile_and_favourite_test.set_up()
profile_and_favourite_test.testprofile()
profile_and_favourite_test.testfavourites()