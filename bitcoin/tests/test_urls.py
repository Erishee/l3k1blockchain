from django.test import SimpleTestCase,Client
from bitcoin.models import Utilisateur, Bloc, Transactions, Inputs, Outputs
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
#from bitcoin.portefeuille import Portefeuille
from bitcoin.views import bitcoin, blockchain_info, afficher_tx
from django.urls import reverse,resolve

"""Test case utilisé pour tester les urls."""
class bitcoinUrlTest(SimpleTestCase):

    def test_url_bitcoin_is_resolved(self):
        url = reverse('bitcoin:bitcoin')
        self.assertEquals(resolve(url).func, bitcoin)

    def test_url_blockchain_info_is_resolved(self):
        url = reverse('bitcoin:blockchain_info')
        self.assertEquals(resolve(url).func, blockchain_info)

    def test_url_transactions_is_resolved(self):
        url = reverse('bitcoin:afficher_tx')
        self.assertEquals(resolve(url).func, afficher_tx)

"""
    def test_url_portefeuille_is_resolved(self):
        url = reverse('bitcoin:portefeuille',args=['1NZgJa5CV4qRaYcDQu5TCCuG63eutVmuxj'])
        self.assertEquals(resolve(url).func, portefeuille)
"""