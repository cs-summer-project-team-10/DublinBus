from django.test import TestCase
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse


from . import views

# Create your tests here.

class IndexPageTests(TestCase):
    def test_index_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_url_by_name(self):
        response = self.client.get(reverse('home_page'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/index.html')

    def test_inedx_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<div id="map"></div>')

    def test_index_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(response, "This should not be contained")


# Test that view returns JSON file in correct format
