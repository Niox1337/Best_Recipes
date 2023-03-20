from django.urls import path
from recipes import views

app_name = 'Best_Recipes'

urlpatterns = [
    path('', views.index, name='index'),
]