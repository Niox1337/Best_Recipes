from django import forms
from django.contrib.auth.models import User
from recipes.models import UserProfile
from recipes.models import UserProfile, Tag, Review, Rating, Recipe


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        help_texts = {
            'username': None,
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'date_of_birth', 'user_description', 'profile_picture')

