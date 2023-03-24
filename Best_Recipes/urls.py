"""Best_Recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from recipes import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name="logout"),
    path('sign_up', views.sign_up, name='sign_up'),
    path('about', views.about, name='about'),
    path('give_rating', views.give_rating, name="give_rating"),
    path('get_rating', views.get_rating, name="get_rating"),
    path('get_recipe_rating', views.get_recipe_rating, name="get_recipe_rating"),
    path('users/<slug:user_name_slug>/recipes/new_recipe', views.new_recipe, name='new_recipe'),
    path('recipes/<slug:recipe_name_slug>/edit_recipe', views.edit_recipe, name='edit_recipe'),
    path('recipes/<slug:recipe_name_slug>/delete', views.delete_recipe, name='delete_recipe'),
    path('recipes/<slug:recipe_name_slug>/delete/true_delete', views.true_delete_recipe, name='true_delete_recipe'),
    path('tags/<slug:tag_name_slug>', views.show_tag, name='show_tag'),
    path('users/<slug:user_name_slug>/',
        views.profile, name='profile'),
    path('users/<slug:user_name_slug>/favourites',
        views.favourites, name='favourites'),
    path('recipes/<slug:recipe_name_slug>/',
        views.show_recipe, name='show_recipe'),
    path('recipes/', include('recipes.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
