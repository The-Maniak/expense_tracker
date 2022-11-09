from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Category, Expense


def index(request):
    """The home page for Expense Tracker"""
    return render(request, 'expense_tracker_app/index.html')


def categories(request):
    """Page where user can see his expenses. Displayed as function."""
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'expense_tracker_app/categories.html', context)


class CategoryView(ListView):
    """Page where user can see his expenses. Displayed as class."""
    model = Category


def category(request, category_id):
    """Page displaying users expenses in a particular category."""
    category = Category.objects.get(id=category_id)
    expenses = Expense.objects.filter(category=category)
    context = {'expenses': expenses}
    return render(request, 'expense_tracker_app/category.html', context)
