from django import forms
from .models import Category, Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']
        labels = {'text': ''}


class ExpenseForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial='Select the category',
#        limit_choices_to=
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date_added = forms.DateField()
    description = forms.CharField(max_length=100)

