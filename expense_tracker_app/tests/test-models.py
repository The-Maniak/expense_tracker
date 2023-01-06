from django.test import TestCase
from django.contrib.auth.models import User
from expense_tracker_app.models import Category, Expense

class CategoryTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_model_create(self):
        # Create a new category
        category = Category.objects.create(text='Food', owner=self.user)

        # Save the category to the database
        category.save()

        # Retrieve the category from the database
        saved_category = Category.objects.get(pk=category.pk)

        # Check that the category was saved to the database correctly
        self.assertEqual(saved_category.text, 'Food')
        self.assertEqual(saved_category.owner, self.user)

    def test_model_update(self):
        # Create a new category
        category = Category.objects.create(text='Food', owner=self.user)

        # Update the category in the database
        category.text = 'Clothing'
        category.save()

        # Retrieve the updated category from the database
        saved_category = Category.objects.get(pk=category.pk)

        # Check that the category was updated in the database correctly
        self.assertEqual(saved_category.text, 'Clothing')
        self.assertEqual(saved_category.owner, self.user)

    def test_model_delete(self):
        # Create a new category
        category = Category.objects.create(text='Food', owner=self.user)

        # Delete the category from the database
        category.delete()

        # Check that the category was deleted from the database
        self.assertEqual(Category.objects.count(), 0)