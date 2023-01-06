from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.widgets import AdminDateWidget
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
import calendar
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
    if request.GET.get('start_of_month'):
        # Set the start and end dates to the beginning and end of the current month
        now = timezone.now()
        start_date = now.replace(day=1)
        end_date = now.replace(day=calendar.monthrange(now.year, now.month)[1])
    else:
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
    # Filter the expenses based on the start and end dates
    if start_date:
        expenses = expenses.filter(date_added__gte=start_date)
    if end_date:
        expenses = expenses.filter(date_added__lte=end_date)
    total_expenses = expenses.aggregate(Sum('amount'))
    total_expenses_amount = total_expenses['amount__sum']
    if total_expenses_amount:
        formatted_total_expenses_amount = f"{total_expenses_amount:.2f}"
    # paginator = Paginator(expenses, 5)  # Show 5 expenses per page
    # page = request.GET.get('page')
    # expenses = paginator.get_page(page)
    if expenses:
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
        context = {'expenses': expenses, 'chart': chart, 'category': category, 'form': DateForm(),
                   'total_expenses_amount': formatted_total_expenses_amount}
    else:
        context = {'expenses': expenses, 'category': category}
    return render(request, 'expense_tracker_app/category.html', context)

@login_required()
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
            return redirect('expense_tracker_app:categories_class')
    context = {'form': form}
    return render(request, 'expense_tracker_app/add_category.html', context)


class AddExpense(CreateView):
    """Add a new expense. Select a category from the list of previously added categories, connected to your user."""
    model = Expense
    fields = ('category', 'amount', 'date_added', 'description')
    context_object_name = 'category_id'

    def get_form(self, form_class=None):
        form = super(AddExpense, self).get_form(form_class)
        form.fields['date_added'].widget = AdminDateWidget(attrs={'type': 'date',})
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

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


class OverviewView(ListView):
    model = Category
    # template_name = 'overview.html'
    context_object_name = 'categories'
    ordering = ('text',)

    def get(self, request):
        categories = Category.objects.filter(owner=self.request.user)
        expenses = Expense.objects.filter(category__in=categories, amount__gte=1)
        expenses_total_amount = expenses.values('category').annotate(sum=Sum('amount'))
        category_labels = [category.text for category in categories]
        expense_values = [expense['sum'] for expense in expenses_total_amount]
        fig = px.pie(
            # labels=category_labels,
            values=expense_values,
        )
        fig.update_traces(
            title_text='Expenses by category in percent',
            title_position='bottom center',
            textposition='inside',
            textinfo='text+percent',
            text=[label for label in category_labels],
            hovertext='percent',
            #showlegend=True,
            automargin=True,
            insidetextorientation='radial',
        )

        chart = fig.to_html()
        context = {
            'categories': categories,
            'chart': chart
        }
        return render(request, 'expense_tracker_app/overview.html', context)
