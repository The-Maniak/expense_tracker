"""Defines URL patterns for users"""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Page for registering new users:
    path('register/', views.register, name='register'),
    # Page for logging in exising users:
    path('login/', views.login, name='login'),
    # Page for users who logged themselves out:
    path('logout/', views.logout, name='logout'),
]