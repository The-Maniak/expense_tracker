from django import forms
from django.utils import timezone
from .models import Category, Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']
        labels = {'text': ''} # Here we can add some text above the inserted category title:
        widgets = {'text': forms.TextInput(attrs={'class': 'form-control'})}



class ExpenseForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=Category.pk,
        # widget=forms.Select(attrs= {'class': 'form-control'}),
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        # widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the start field to the date of the earliest expense in the database
        earliest_expense = Expense.objects.order_by('date_added').first()
        if earliest_expense:
            self.fields['start'].initial = earliest_expense.date_added
        # Set the end field to today's date
        now = timezone.now()
        self.fields['end'].initial = now

