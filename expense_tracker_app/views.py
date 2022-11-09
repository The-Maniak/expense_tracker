from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Category, Expense


def index(request):
    """The home page for Expense Tracker"""
    return render(request, 'expense_tracker_app/index.html')


def categories(request):
    """Page where user can see his expenses."""
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'expense_tracker_app/categories.html', context)

class CategoryView(ListView):
    model = Category


