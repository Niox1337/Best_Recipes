from django.test import TestCase
from datetime import date
from django.urls import reverse
from recipes.models import UserProfile, Recipe, Review, Rating
import populate_recipes

'''
Unit tests for models:
UserProfile
Recipe
Review
Rating
'''

class SignUpTest(TestCase):
    def test_if_sign_up_adds_user(self):
        """""
        Adding a test user and checking if the information has been added to the database
        """""
        info_dict={
            "first_name":"testFirstName",
            "last_name":"testLastName",
            "email":"testEmail",
            "dateOfBirth":date.today(),
            "password":"testPassword",
            "user_description":"testUserDescription",
            "profile_picture":"testProfilePicture",
            "user_name":"testUserName",
        }
        add_user_profile(info_dict)
        self.assertEqual(info_dict,)



class RatingsTest(TestCase):
    def test_ensure_ratings_are_positive(self)
    """
    Ensures the number of ratings received for a recipe are positive or zero
    """
    rating = add_rating(info_dict)
    self.assertEquals(rating.rating>=0, True)


    


'''
Unit Tests for views:
    index
    login
    sign_up
    about
'''
class TestViews(TestCase):
    def test_index(self):
        """check status code is 200"""
        """status code 200 means response is successful"""

        response = self.client.get(reverse('recipe:index'))

        self.assertEqual(response.status_code, 200)

    def test_about(self):
        """check status code is 200"""

        response = self.client.get(reverse('recipe:about'))

        self.assertEqual(response.status_code,200) 

