from django.test import TestCase
from django.urls import reverse
from expense_tracker_app.models import Category, Expense

class IndexViewTestCase(TestCase):
    def test_index_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('index'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

class CategoriesViewTestCase(TestCase):
    def setUp(self):
        # Create some test categories
        Category.objects.create(name='Food', owner=self.user)
        Category.objects.create(name='Entertainment', owner=self.user)

    def test_categories_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('categories'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct categories are included in the response context
        self.assertEqual(len(response.context['categories']), 2)
        self.assertQuerysetEqual(response.context['categories'], ['<Category: Food>', '<Category: Entertainment>'])

class CategoryOverviewViewTestCase(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name='Food', owner=self.user)

        # Create some test expenses
        Expense.objects.create(description='Groceries', amount=20.00, date_added='2022-01-01', category=self.category)
        Expense.objects.create(description='Restaurant', amount=50.00, date_added='2022-01-02', category=self.category)

    def test_category_overview_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('category', args=[self.category.id]))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct expenses are included in the response context
        self.assertEqual(len(response.context['expenses']), 2)
        self.assertQuerysetEqual(response.context['expenses'], ['<Expense: Groceries>', '<Expense: Restaurant>'])