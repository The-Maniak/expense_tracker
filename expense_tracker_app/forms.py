from django import forms
from .models import Category #, Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']
        labels = {'text': ''}


class ExpenseForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=Category.pk
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(max_length=100)


class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

