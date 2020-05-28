from django.test import TestCase
from ethereum.models import Utilisateur,Transactions
from ethereum.ethusers import EthUsers
"""Test case utilisé pour tester views ETH."""
class Test_method_ETH(TestCase):
    databases = '__all__'
    @classmethod
    def setUpTestData(cls):
        Utilisateur.objects.db_manager('ethereum').create(address="test_adr_source",
                                   eth_balance=100)
        u_s = Utilisateur.objects.db_manager('ethereum').get(address = "test_adr_source")
        Utilisateur.objects.db_manager('ethereum').create(address="test_adr_destination",
                                   eth_balance=200)
        u_d = Utilisateur.objects.db_manager('ethereum').get(address = "test_adr_destination")
        Utilisateur.objects.db_manager('ethereum').create(address="test_adr1",
                                   eth_balance=300)
        u_test = Utilisateur.objects.db_manager('ethereum').get(address = "test_adr1")
        Transactions.objects.db_manager('ethereum').create(hash_field = "test_hash",
                                    timestamp_field = "2019-01-02",
                                    block_number = 600000,
                                    source = "test_adr_source",
                                    destination = "test_adr_destination",
                                    value = 100)
        tx_eth1 = Transactions.objects.db_manager('ethereum').get(hash_field = "test_hash")

    def test_get_allusers(self):
        u_s = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_source")
        u_d = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_destination")
        u_test = Utilisateur.objects.db_manager('ethereum').get(address="test_adr1")
        self.assertEqual(3,len(EthUsers.get_allusers()))

    def test_get_users(self):
        u_s = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_source")
        u_d = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_destination")
        u_test = Utilisateur.objects.db_manager('ethereum').get(address="test_adr1")
        self.assertEqual(3,len(EthUsers.get_users()))
        self.assertEqual("test_adr_source",EthUsers.get_users()[0])

    def test_echange(self):
        u_s = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_source")
        u_d = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_destination")
        u_test = Utilisateur.objects.db_manager('ethereum').get(address="test_adr1")
        tx_eth1 = Transactions.objects.db_manager('ethereum').get(hash_field = "test_hash")
        self.assertEqual(1,len(EthUsers.echanges(EthUsers.get_users())))
        self.assertEqual(("test_adr_source","test_adr_destination",100,"2019-01-02"),EthUsers.echanges(EthUsers.get_users())[0])

    def test_echanges_index_et_test_valeurs(self):
        u_s = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_source")
        u_d = Utilisateur.objects.db_manager('ethereum').get(address="test_adr_destination")
        u_test = Utilisateur.objects.db_manager('ethereum').get(address="test_adr1")
        tx_eth1 = Transactions.objects.db_manager('ethereum').get(hash_field = "test_hash")
        test_utilisateur = EthUsers.get_users()
        test_echange = EthUsers.echanges(EthUsers.get_users())
        self.assertEqual(0, EthUsers.valeurs(test_utilisateur,test_echange).get('links')[0].get('source'))
        self.assertEqual(100, EthUsers.valeurs(test_utilisateur, test_echange).get('links')[0].get('value'))


