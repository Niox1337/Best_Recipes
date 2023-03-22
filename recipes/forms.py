from django import forms
from django.contrib.auth.models import User
from recipes.models import UserProfile
from recipes.models import UserProfile, Tag, Review, Rating, Recipe

class RegisterForm(forms.ModelForm):
    user_name = forms.CharField(max_length=UserProfile.USER_NAME_LEN,
                                help_text="User Name")
    
    class Meta:
        model = UserProfile
        fields = [
            'user_name',
        ]


class LoginForm(forms.ModelForm):
    pass

class EditRecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=Recipe.NAME_LEN,
                           help_text="Recipe Name")
    ingredients = forms.TextInput()
    text = forms.TextInput()
   
    class Meta:
        model = Recipe
        fields = [
            'name',
            "ingredients",
            "text",
        ]
