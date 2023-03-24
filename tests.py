import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'Best_Recipes.settings')
import django
django.setup()
from django.test import TestCase, Client
from datetime import date
from django.urls import reverse
from recipes.models import UserProfile, Recipe, Review, Rating
import population_script


'''
Unit tests for models:
UserProfile
Recipe
Review
Rating
'''

class SignUpTest(TestCase):

    def setUp(self):
       info_dict={
            "first_name":"testFirstName",
            "last_name":"testLastName",
            "email":"testEmail",
            "dateOfBirth":date.today(),
            "password":"testpassword",
            "user_description":"testUserDescription",
            "profile_picture":"testProfilePicture",
            "user_name":"testuser",
            }
        


    def test_if_sign_up_adds_user(self):
        """""
        Adding a test user and checking if the information has been added to the database
        """""
        info_dict={
            "first_name":"testFirstName",
            "last_name":"testLastName",
            "email":"testEmail",
            "dateOfBirth":date.today(),
            "password":"testpassword",
            "user_description":"testUserDescription",
            "profile_picture":"testProfilePicture",
            "user_name":"testuser",
        }
        add_user_profile(info_dict)
        self.assertEqual(str(self.user), 'test_user')

    def test_max_lengths(self):
        self.assertEqual(
            self.user._meta.get_field('user_name').max_length, 
            UserProfile.USER_NAME_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('first_name').max_length, 
            UserProfile.FIRST_NAME_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('last_name').max_length, 
            UserProfile.LAST_NAME_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('email').max_length, 
            UserProfile.EMAIL_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('password').max_length, 
            UserProfile.PASSWORD_LEN
        )
        self.assertEqual(
            self.user._meta.get_field('user_description').max_length, 
            UserProfile.USER_DESCRIPTION_LEN
        )

    def test_default_reviews(self):
        """
        Check the recipe initially has zero reviews
        """
        test_recipe_one = {
        "keys": {
            "creator": USER_ONE_USERNAME,
            "savedBy": [USER_THREE_USERNAME]
        },
        "other": {
            "name": "testName",
            "text": "testText",
            "noOfRatings": 0,
            "recipePicture": None,
            "id": 1,
            "views": 0
        }
        }

class RatingsTest(TestCase):
    def test_ensure_ratings_are_positive(self):
        """
        Ensures the number of ratings received for a recipe are positive or zero
        """
        rating = add_rating(info_dict)
        self.assertEquals(rating.rating>=0, True)

    

'''
-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
Unit Tests for views:
    index
    user_login
    user_logout
    sign_up
    edit_recipe
    new_recipe
    show_recipe
    about
    profile
    favourites
'''
class IndexAboutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        """check status code is 200"""
        """status code 200 means response is successful"""
        response = self.client.get(reverse('recipe:index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('recipe:about'))
        self.assertEqual(response.status_code,200) 

class UserLogInAndLogOut(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=add_user_profile(info_dict)
    
    def test_user_login_get(self):
        response = self.client.get(reverse("recipes:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/login.html")

    def test_user_login_post(self):
        response = self.client.post(reverse("recipes:login"), {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertRedirects(response, reverse("recipes:index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_post_invalid(self):
        response = self.client.post(reverse("recipes:login"), {
            "username": "testuser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/login.html")
        self.assertContains(response, "Invalid username or password")

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/index.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_logout_redirects_to_login(self):
        response = self.client.get(reverse('recipes:logout'))
        self.assertRedirects(response, reverse('recipes:login'))

class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse('recipes:sign_up')

    def test_sign_up_view_with_valid_data(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        }
        profile_data = {
            'website': 'http://example.com',
        }
        response = self.client.post(self.sign_up_url, {
            'user_form': UserForm(user_data),
            'profile_form': UserProfileForm(profile_data),
        })
        '''
        verify that the user and profile were created
        '''
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['registered'])
        self.assertTrue(User.objects.filter(username=user_data['username']).exists())
        self.assertTrue(UserProfile.objects.filter(user__username=user_data['username']).exists())


    def test_sign_up_view_with_invalid_data(self):
        '''
        Creating invalid form data to verify that form errors are displayed
        '''
        user_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'testpassword',
            'confirm_password': 'differentpassword',
        }
        profile_data = {
            'website': 'invalid-website',
        }

        response = self.client.post(self.sign_up_url, {
            'user_form': UserForm(user_data),
            'profile_form': UserProfileForm(profile_data),
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['registered'])
        self.assertFormError(response, 'user_form', 'email', 'Enter a valid email address.')
        self.assertFormError(response, 'user_form', 'confirm_password', 'Passwords do not match.')
        self.assertFormError(response, 'profile_form', 'website', 'Enter a valid URL.')

class RecipeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(creator=self.user.profile, name='Test Recipe', text='This is a test recipe.', views=0, ingredients='Test Ingredient 1, Test Ingredient 2', no_of_ratings=0)
        self.tag1 = Tag.objects.create(tag='Test Tag 1')
        self.tag2 = Tag.objects.create(tag='Test Tag 2')
        self.recipe.tags.add(self.tag1, self.tag2)
        self.recipe.save()

    def test_edit_recipe(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_recipe', args=[self.recipe.recipe_name_slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/edit_recipe.html')
        self.assertIsInstance(response.context['edit_recipe_form'], EditRecipeForm)
        self.assertQuerysetEqual(response.context['tags'], Tag.objects.all(), ordered=False)
        self.assertEqual(response.context['recipe_creator'], self.user.profile.user_name_slug)

    def test_edit_recipe_with_valid_form(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_recipe', args=[self.recipe.recipe_name_slug])
        data = {
            'name': 'Updated Test Recipe',
            'text': 'This is an updated test recipe.',
            'views': 5,
            'ingredients': 'Updated Ingredient 1, Updated Ingredient 2',
            'no_of_ratings': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/edit_recipe.html')
        self.assertEqual(response.context['recipe_creator'], self.user.profile.user_name_slug)
        self.assertTrue(Recipe.objects.filter(name='Updated Test Recipe').exists())

    def test_edit_recipe_with_invalid_form(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_recipe', args=[self.recipe.recipe_name_slug])
        data = {
            'name': '',
            'text': 'This is an updated test recipe.',
            'views': 5,
            'ingredients': 'Updated Ingredient 1, Updated Ingredient 2',
            'no_of_ratings': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/edit_recipe.html')
        self.assertContains(response, 'This field is required.')
        self.assertEqual(response.context['recipe_creator'], self.user.profile.user_name_slug)

    def test_delete_recipe(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('delete_recipe', args=[self.recipe.recipe_name_slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/delete_recipe.html')
        self.assertEqual(response.context['recipe'], self.recipe)


class ProfileAndFavouritesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('profile', kwargs={'user_name_slug': slugify(self.user.username)})
        self.url = reverse('favourites', kwargs={'user_name_slug': slugify(self.user.username)})

    def testprofile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def testfavourites(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)