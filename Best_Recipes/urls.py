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
    path('sign_up', views.sign_up, name='sign_up'),
    path('about', views.about, name='about'),
    path('edit_recipe', views.edit_recipe, name='edit_recipe'),
    path('users/<slug:user_name_slug>/',
        views.profile, name='profile'),
    path('recipes/<slug:recipe_name_slug>/',
        views.show_recipe, name='show_recipe'),
    path('recipes/', include('recipes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
