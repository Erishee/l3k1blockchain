from django.test import TestCase, Client
from ethereum.views import ethereum,afficher_tx_eth,portefeuille_eth
from django.urls import reverse,resolve
from ethereum.models import Utilisateur,Transactions

"""Test case utilisé pour tester views ETH."""
class TestViews_ETH(TestCase):
    databases = '__all__'
    @classmethod
    def setUpTestData(cls):
        Utilisateur.objects.db_manager('ethereum').create(address="test_adr_source",
                                   eth_balance=100)
        u_s = Utilisateur.objects.db_manager('ethereum').get(address = "test_adr_source")
        Utilisateur.objects.db_manager('ethereum').create(address="test_adr_destination",
                                   eth_balance=100)
        u_d = Utilisateur.objects.db_manager('ethereum').get(address = "test_adr_destination")
        Transactions.objects.db_manager('ethereum').create(hash_field = "test_hash",
                                    timestamp_field = "2019-01-02",
                                    block_number = 600000,
                                    source = "test_adr_source",
                                    destination = "test_adr_destination",
                                    value = 100)
        tx_eth = Transactions.objects.db_manager('ethereum').get(hash_field = "test_hash")
    def test_ethereum_view(self):
        client = Client()
        response = client.get(reverse('ethereum:ethereum'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ethereum/ethereum.html')

    def test_afficher_tx_eth_view(self):
        client = Client()
        response = client.get(reverse('ethereum:afficher_tx_eth'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ethereum/transactions_eth.html')

    def test_portefeuille_eth_view(self):
        client = Client()
        response = client.get(reverse('ethereum:portefeuille_eth',args = ['test_adr_source']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ethereum/portefeuille_eth.html')