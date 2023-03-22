from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('about/', views.about, name='about'),
]