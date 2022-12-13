from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.widgets import AdminDateWidget
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import plotly.express as px
from .models import Category, Expense
from .forms import CategoryForm, DateForm, ExpenseForm


def index(request):
    """The home page for Expense Tracker"""
    return render(request, 'expense_tracker_app/index.html')


@login_required()
def categories(request):
    """Page where user can see his expenses. Displayed as function."""
    categories = Category.objects.filter(owner=request.user)  # all() Tu trzeba jeszcze przefiltrowac po Userze
    context = {'categories': categories}
    return render(request, 'expense_tracker_app/categories.html', context)


class CategoryView(ListView):
    """Page where user can see his expenses. Displayed as class.
    The @login_required decorator for the class view is applied in the views.py file."""
    model = Category

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


@login_required()
def category(request, category_id):
    """Page displaying users expenses in a particular category."""
    category = Category.objects.get(id=category_id)
    if category.owner != request.user:
        raise Http404
    expenses = Expense.objects.filter(category=category)
    if expenses:
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start:
            expenses = expenses.filter(date_added__gte=start)
        if end:
            expenses = expenses.filter(date_added__lte=end)
        fig = px.bar(
            x=[expense.date_added for expense in expenses],
            y=[expense.amount for expense in expenses],
            labels={
                'x': "Date",
                'y': 'Amount PLN',
            },
            text=[expense.description for expense in expenses],

        )
        fig.update_layout(title_text='Expenses in this categoory:')
        chart = fig.to_html()
        context = {'expenses': expenses, 'chart': chart, 'category': category, 'form': DateForm()}
    else:
        context = {'expenses': expenses, 'category': category}
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
            return redirect(
                'expense_tracker_app:index')  # Poprawić to przekierowanie gdy zdecyduję się czy kategorie będą wyświetlane z widoku klasy czy z widoku funkcji.
    context = {'form': form}
    return render(request, 'expense_tracker_app/add_category.html', context)


class AddExpense(CreateView):
    """Add a new expense. Select a category from the list of previously added categories, connected to your user."""
    model = Expense
    fields = ('category', 'amount', 'date_added', 'description')
    context_object_name = 'category_id'
    #    form_class = ExpenseForm
    #success_url = '/' # trzeba poprawic

    def get_form(self, form_class=None):
        form = super(AddExpense, self).get_form(form_class)
        form.fields['date_added'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['category'].limit_choices_to = {'owner_id': self.request.user}
        return modelform

    def get_success_url(self):
        expense = self.object
        category_id = expense.category.pk
        return reverse('expense_tracker_app:category', kwargs={'category_id': category_id})


class EditExpense(UpdateView):
    """Edit a previously added expense."""
    model = Expense
    pk_url_kwarg = 'expense_id'
    fields = ('category', 'amount', 'date_added', 'description')

    def get_success_url(self):
        expense = self.get_object()
        category_id = expense.category.pk
        return reverse_lazy('expense_tracker_app:category', kwargs={'category_id': category_id})


class DeleteExpense(DeleteView):
    """Delete a previously added expense."""
    model = Expense
    pk_url_kwarg = 'expense_id'

    def get_success_url(self):
        expense = self.get_object()
        category_id = expense.category.pk
        return reverse_lazy('expense_tracker_app:category', kwargs={'category_id': category_id})
