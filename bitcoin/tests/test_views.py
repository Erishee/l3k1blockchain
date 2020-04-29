from django.test import TestCase, Client
from bitcoin.models import Utilisateur, Bloc, Transactions, Inputs, Outputs
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
from bitcoin.portefeuille import Portefeuille
from django.urls import reverse

"""Test case utilisé pour tester views.py."""
class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
            Utilisateur.objects.create(
                adresse = "test_adr1",
                nb_tx= 1,
                total_recu = 200,
                total_envoye = 100,
                solde_final = 100,
                nb_bcalcules = 1
            )
            Utilisateur.objects.create(
                adresse = "test_adr2",
                nb_tx= 2,
                total_recu = 300,
                total_envoye = 100,
                solde_final = 200,
                nb_bcalcules = 2
            )
            Utilisateur.objects.create(
                adresse = "test_adr3",
                nb_tx= 3,
                total_recu = 500,
                total_envoye = 200,
                solde_final = 300,
                nb_bcalcules = 3
            )
            u1 = Utilisateur.objects.get(adresse = "test_adr1")
            u2 = Utilisateur.objects.get(adresse = "test_adr2")
            u3 = Utilisateur.objects.get(adresse = "test_adr3")
            Transactions.objects.create(hash_tx = "test_hash_tx1",
                                        date = "2015-2-12",
                                        hauteur = 600001,
                                        adresse = u1
            )
            Transactions.objects.create(hash_tx = "test_hash_tx2",
                                        date = "2016-3-13",
                                        hauteur = 600002,
                                        adresse = u2
            )
            Transactions.objects.create(hash_tx = "test_hash_tx3",
                                        date = "2017-10-20",
                                        hauteur = 600003,
                                        adresse = u3
            )
            tx1 = Transactions.objects.get(hash_tx = "test_hash_tx1")
            tx2 = Transactions.objects.get(hash_tx = "test_hash_tx2")
            tx3 = Transactions.objects.get(hash_tx = "test_hash_tx3")
            Bloc.objects.create(hauteur=600001,
                                hash_bloc="test_hash_bloc1",
                                adresse=u1,
                                nb_tx="1000")
            Bloc.objects.create(hauteur=600002,
                                hash_bloc="test_hash_bloc2",
                                adresse=u2,
                                nb_tx="2000")
            Bloc.objects.create(hauteur=600003,
                                hash_bloc="test_hash_bloc3",
                                adresse=u3,
                                nb_tx="3000")
            b1 = Bloc.objects.get(hauteur=600001)
            b2 = Bloc.objects.get(hauteur=600002)
            b3 = Bloc.objects.get(hauteur=600003)
    def test_bitcoin_view(self):
        client = Client()

        response = client.get(reverse('bitcoin:bitcoin'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'bitcoin/bitcoin.html')

    def test_portefeuille_view(self):
        client = Client()

        response = client.get(reverse('bitcoin:portefeuille',args = ['test_adr1']))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'bitcoin/portefeuille.html')

    def test_blockchain_info_view(self):
        client = Client()

        response = client.get(reverse('bitcoin:blockchain_info'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'bitcoin/blockchain_info.html')

    def test_afficher_tx_view(self):
        client = Client()

        response = client.get(reverse('bitcoin:afficher_tx'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'bitcoin/transactions.html')