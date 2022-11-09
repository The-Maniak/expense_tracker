"""Defines URL patterns for Expense Tracker App"""
from django.urls import path
from . import views

app_name= 'expense_tracker_app'
urlpatterns =[
    # Home page:
    path('', views.index, name='index'),
    # Expense categories page (function):
    path('categories_function/', views.categories, name='categories_function'),
    # Expense categories page (class):
    path('categories_class/', views.CategoryView.as_view(), name='categories_class'),
]