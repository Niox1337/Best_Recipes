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
    picture = forms.ImageField(label="Profile Picture")

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'date_of_birth', 'user_description', 'picture',)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class EditRecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=Recipe.NAME_LEN,
                           help_text="Recipe Name")
    ingredients = forms.TextInput()
    text = forms.TextInput()
    western = forms.CheckboxInput()
    asian = forms.CheckboxInput()
    indian = forms.CheckboxInput()
    chinese = forms.CheckboxInput()
    african = forms.CheckboxInput()
    american = forms.CheckboxInput()
    other = forms.CheckboxInput()

    class Meta:
        model = Recipe
        fields = [
            'name',
            "ingredients",
            "text",
            "western",
            "asian",
            "indian",
            "chinese",
            "african",
            "american",
            "other",
        ]
