from django.test import TestCase, Client
from contact.views import contact,about
from django.urls import reverse,resolve
from contact.models import Contact

"""Test case utilisé pour tester views.py."""
class ContactTestViews(TestCase):

    def test_about_us_view(self):
        client = Client()
        response = client.get(reverse('contact:about'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'contact/aboutus.html')

    def test_contact_us_view(self):
        client = Client()
        response = client.get(reverse('contact:contact'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'contact/contact.html')
