from django.test import SimpleTestCase,Client
from contact.views import contact,about
from django.urls import reverse,resolve
from contact.models import Contact

"""Test case utilisé pour tester les urls_contact."""
class contactUrlTest(SimpleTestCase):

    def test_url_bitcoin_is_resolved(self):
        url = reverse('contact:contact')
        self.assertEquals(resolve(url).func, contact)

    def test_url_blockchain_info_is_resolved(self):
        url = reverse('contact:about')
        self.assertEquals(resolve(url).func, about)