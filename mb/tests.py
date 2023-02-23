from django.test import TestCase
from django.test import Client
from django.urls import reverse

class Pages_loads_ok_Tests(TestCase):
    def setUp(self):
        # I need a client to see what i get.
        self.client = Client()

    def test_homepage_loads_ok(self):
        """
        Check if the homepage loads.
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200) # 200 OK

    def test_loginpage_loads_ok(self):
        """
        Check if the login page loads.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200) # 301 REDIRECTION

    def test_logged_out_page_loads_ok(self):
        """
        Check if the logged_out page loads.
        """
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
