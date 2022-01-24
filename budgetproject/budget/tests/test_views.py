import json
from django.http import response
from django.test import TestCase, Client, client
from django.urls import reverse
from budget.models import *

# Create your tests here.



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.project1 = Project.objects.create(name='project1', budget=100)
        self.detail_url = reverse('detail', args=['project1'])


    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    
    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    
    def test_project_detail_POST_adds_new_expense(self):
        Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().title, 'expense1')
        self.assertEqual(Expense.objects.first().amount, 1000)
        self.assertEqual(Expense.objects.first().category.name, 'development')


    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 0)


    def test_project_detail_DELETE_removes_expense(self):

        Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = Category.objects.first()
        )

        response = self.client.delete(self.detail_url, json.dumps({'id': Expense.objects.first().id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Expense.objects.count(), 0)

    

    def test_project_detail_DELETE_no_id_expense(self):

        Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = Category.objects.first()
        )

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Expense.objects.count(), 1) 


    def test_project_create_POST(self):
        response = self.client.post(reverse('add'), {
            'name': 'project2',
            'budget': 1000,
            'categoriesString': 'development, marketing'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.last().name, 'project2')
        self.assertEqual(Project.objects.last().budget, 1000)
        first_category = Category.objects.get(id=1)
        self.assertEqual(first_category.project.name, 'project2')
        self.assertEqual(first_category.name, 'development')
        self.assertEqual(Category.objects.filter(project=Project.objects.get(id=2)).count(), 2)














# python manage.py test budget.tests.test_views



