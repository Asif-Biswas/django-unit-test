
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from budget.views import *


class TestUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func, project_list)

    
    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)

    
    def test_detail_url_resolves(self):
        url = reverse('detail', args=['some-slug'])
        self.assertEqual(resolve(url).func, project_detail)
