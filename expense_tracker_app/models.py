from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Category(models.Model):
    """A category of expenses."""
    text = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a string presentation of the model"""
        return self.text


class Expense(models.Model):
    """Individual expenses inserted in the tracker."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(default=now())
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'expenses'

    def __str__(self):
        return f"{self.date_added} - {self.category} - {self.description} - {self.amount}"
