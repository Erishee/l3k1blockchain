from django.test import TestCase
from ethereum.models import Utilisateur,Transactions

"""Test case utilisé pour tester les ethereum models."""
class Eth_ModelTest(TestCase):
    databases = '__all__'
    @classmethod
    def setUp(self):
        Utilisateur.objects.create(address="test_adr_source",
                                   eth_balance=100)

        Utilisateur.objects.create(address="test_adr_destination",
                                   eth_balance=100)

        Transactions.objects.create(hash_field = "test_hash",
                                    timestamp_field = 12345678,
                                    block_number = 600000,
                                    source = "test_adr_source",
                                    destination = "test_adr_destination",
                                    value = 100)

    def test_adresse_utilisateur_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        field_label = Utilisateur._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')
        max_length = u_s._meta.get_field('address').max_length
        self.assertEquals(max_length, 300)

    def test_eth_balance_utilisateur_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_destination")
        field_label = Utilisateur._meta.get_field('eth_balance').verbose_name
        self.assertEquals(field_label, 'eth balance')

    def test_hash_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('hash_field').verbose_name
        self.assertEquals(field_label, 'hash field')

    def test_timestamp_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('timestamp_field').verbose_name
        self.assertEquals(field_label, 'timestamp field')

    def test_block_number_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('block_number').verbose_name
        self.assertEquals(field_label, 'block number')

    def test_source_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('source').verbose_name
        self.assertEquals(field_label, 'source')

    def test_destination_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('destination').verbose_name
        self.assertEquals(field_label, 'destination')

    def test_value_eth(self):
        u_s = Utilisateur.objects.get(address="test_adr_source")
        u_d = Utilisateur.objects.get(address="test_adr_destination")
        tx_eth = Transactions.objects.get(hash_field = "test_hash")

        field_label = Transactions._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'value')