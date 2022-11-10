from django import forms
from .models import Category, Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']
        labels = {'text': ''}


# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = '__all__'

