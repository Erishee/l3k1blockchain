from django.test import SimpleTestCase,Client
from ethereum.views import ethereum,afficher_tx_eth,portefeuille_eth
from django.urls import reverse,resolve
from ethereum.models import Utilisateur,Transactions

"""Test case utilisé pour tester les urls_ethereum."""
class EthUrlTest(SimpleTestCase):
    databases = '__all__'
    def test_url_ethereum_is_resolved(self):
        url = reverse('ethereum:ethereum')
        self.assertEquals(resolve(url).func, ethereum)

    def test_url_afficher_tx_eth_is_resolved(self):
        url = reverse('ethereum:afficher_tx_eth')
        self.assertEquals(resolve(url).func, afficher_tx_eth)

    def test_url_portefeuille_eth_is_resolved(self):
        url = reverse('ethereum:portefeuille_eth',args=['0x742d35cc6634c0532925a3b844bc454e4438f44e'])
        self.assertEquals(resolve(url).func, portefeuille_eth)