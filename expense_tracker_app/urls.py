"""Defines URL patterns for Expense Tracker App"""
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'expense_tracker_app'
urlpatterns = [
    # Home page:
    path('', views.index, name='index'),
    # Expense categories page (function):
    path('categories_function/', views.categories, name='categories_function'),
    # Expense categories page (class):
    path('categories_class/', login_required(views.CategoryView.as_view()), name='categories_class'),
    # Individual expenses page per category:
    path('category/<int:category_id>/', views.category, name='category'),
    # Page for adding new categories of expenses:
    path('add_category/', views.add_category, name='add_category'),
    # Page for adding new expenses:
    # path('add_expense/', views.add_expense, name='add_expense'),
    path('add_expense/', login_required(views.AddExpense.as_view()), name='add_expense'),
    # Page for editing existing expenses:
    path('edit_expense/<int:expense_id>/', login_required(views.EditExpense.as_view()), name='edit_expense'),
    # Page for deleting existing expenses:
    path('delete_expense/<int:expense_id>/', login_required(views.DeleteExpense.as_view()), name='delete_expense'),
]
