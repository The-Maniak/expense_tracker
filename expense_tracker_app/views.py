from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Category, Expense
from .forms import CategoryForm


def index(request):
    """The home page for Expense Tracker"""
    return render(request, 'expense_tracker_app/index.html')


@login_required()
def categories(request):
    """Page where user can see his expenses. Displayed as function."""
    categories = Category.objects.filter(owner=request.user) #all() Tu trzeba jeszcze przefiltrowac po Userze
    context = {'categories': categories}
    return render(request, 'expense_tracker_app/categories.html', context)


class CategoryView(ListView):
    """Page where user can see his expenses. Displayed as class.
    The @login_required decorator for the class view is applied in the views.py file."""
    model = Category


@login_required()
def category(request, category_id):
    """Page displaying users expenses in a particular category."""
    category = Category.objects.get(id=category_id)
    if category.owner != request.user:
        raise Http404
    expenses = Expense.objects.filter(category=category)
    context = {'expenses': expenses}
    return render(request, 'expense_tracker_app/category.html', context)


def add_category(request):
    """Add a new category of expenses."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CategoryForm()
    else:
        # POST the form, add the category.
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect('expense_tracker_app:index') # Poprawić to przekierowanie gdy zdecyduję się czy kategorie będą wyświetlane z widoku klasy czy z widoku funkcji.
    context = {'form': form}
    return render(request, 'expense_tracker_app/add_category.html', context)
