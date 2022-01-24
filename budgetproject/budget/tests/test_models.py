
from django.test import TestCase

from budget.models import *#Category, Expense, Project


class TestModels(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create(
            name='Project 1',
            budget='2000'
        )
        
        category = Category.objects.create(project=self.project1, name='development')
        Expense.objects.create(project=self.project1, title='Development', amount='500', category=category)

    
    def test_budget_left_of_project(self):
        self.assertEqual(self.project1.budget_left, 1500)


    def test_total_transactions_of_project(self):
        self.assertEqual(self.project1.total_transactions, 1)


    def test_get_absolute_url_of_project(self):
        self.assertEqual(self.project1.slug, 'project-1')