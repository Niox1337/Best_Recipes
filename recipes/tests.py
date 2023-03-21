from django.test import TestCase
from datetime import date
from recipes.models import UserProfile

# Create your tests here.
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
        self.assertEquals(info_dict,)

class RatingsTest(TestCase):
    
