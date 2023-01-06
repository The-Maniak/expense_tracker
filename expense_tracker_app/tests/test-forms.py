from django.test import TestCase
from expense_tracker_app.forms import CategoryForm, ExpenseForm, DateForm


class CategoryFormTestCase(TestCase):
    def test_form_valid(self):
        # Create a valid form data dictionary
        form_data = {'text': 'Food'}

        # Create a form instance using the form data
        form = CategoryForm(data=form_data)

        # Check that the form is valid
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Create an invalid form data dictionary
        form_data = {'text': ''}

        # Create a form instance using the form data
        form = CategoryForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())


class ExpenseFormTestCase(TestCase):
    def test_form_valid(self):
        # Create a valid form data dictionary
        form_data = {'category': 1, 'amount': 20.00, 'date_added': '2022-01-01', 'description': 'Groceries'}

        # Create a form instance using the form data
        form = ExpenseForm(data=form_data)

        # Check that the form is valid
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Create an invalid form data dictionary
        form_data = {'category': self.category, 'amount': '', 'date_added': '2022-01-01', 'description': 'Groceries'}

        # Create a form instance using the form data
        form = ExpenseForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())
