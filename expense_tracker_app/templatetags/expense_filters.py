from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_expenses(category):
    total_amount_of_expenses = category.expense_set.all().aggregate(Sum('amount'))['amount__sum']
    if total_amount_of_expenses:
        total_amount_of_expenses = f"{total_amount_of_expenses:.2f}"
    return total_amount_of_expenses