from django.test import TestCase, Client, SimpleTestCase
from accueil.views import accueilBTC,accueilETH
from django.urls import reverse,resolve

"""Test case utilisé pour tester les views accueil."""
class Test_unitaire_accueil(TestCase):
    multi_db = True
    def test_accueil_btc_view(self):
        client = Client()
        response = client.get(reverse('accueil:accueil_btc'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'accueil/accueil.html')
    """
    def test_accueil_eth_view(self):
        client = Client()
        response = client.get(reverse('accueil:accueil_eth'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'accueil/accueil.html')
    """

"""Test case utilisé pour tester les urls_accueil."""
class accueilUrlTest(SimpleTestCase):

    def test_url_accueil_btc_is_resolved(self):
        url = reverse('accueil:accueil_btc')
        self.assertEquals(resolve(url).func, accueilBTC)


    def test_url_accueil_eth_is_resolved(self):
        url = reverse('accueil:accueil_eth')
        self.assertEquals(resolve(url).func, accueilETH)