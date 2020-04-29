from django.test import TestCase
import psycopg2
import datetime
from datetime import datetime
import csv
from datetime import date
from bitcoin.models import Utilisateur, Bloc, Transactions, Inputs, Outputs
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
from bitcoin.portefeuille import Portefeuille
from django.conf import settings
from django.urls import reverse

"""Test case utilisé pour tester les bloc models."""
class BlocModelTest(TestCase):
    @classmethod
    def setUp(self):
        Utilisateur.objects.create(adresse="test_adr",
                                   nb_tx=100,
                                   total_recu=300,
                                   total_envoye=200,
                                   solde_final=100,
                                   nb_bcalcules=100)
        u = Utilisateur.objects.get(adresse="test_adr")
        Bloc.objects.create(hauteur=60000,
                            hash_bloc="test_hash_bloc",
                            adresse=u,
                            nb_tx="3000")
    def test_hauteur_bloc(self):
        block = Bloc.objects.get(hauteur=60000)
        field_label = block._meta.get_field('hauteur').verbose_name
        self.assertEquals(field_label, 'hauteur')

    def test_hash_bloc_bloc(self):
        block = Bloc.objects.get(hauteur=60000)
        field_label = block._meta.get_field('hash_bloc').verbose_name
        self.assertEquals(field_label, 'hash bloc')
        max_length = block._meta.get_field('hash_bloc').max_length
        self.assertEquals(max_length, 100)

    def test_adresse_bloc(self):
        block = Bloc.objects.get(hauteur=60000)
        field_label = block._meta.get_field('adresse').verbose_name
        self.assertEquals(field_label, 'adresse')

    def test_nb_tx_bloc(self):
        block = Bloc.objects.get(hauteur=60000)
        field_label = block._meta.get_field('nb_tx').verbose_name
        self.assertEquals(field_label, 'nb tx')

"""Test case utilisé pour tester les utilisateur models."""
class UtilisateurModelTest(TestCase):
    @classmethod
    def setUp(self):
        # Set up non-modified objects used by all test methods
        Utilisateur.objects.create(adresse="test_adr",
                                   nb_tx=100,
                                   total_recu=300,
                                   total_envoye=200,
                                   solde_final=100,
                                   nb_bcalcules=100)

    def test_adresse_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('adresse').verbose_name
        self.assertEquals(field_label, 'adresse')

    def test_nb_tx_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('nb_tx').verbose_name
        self.assertEquals(field_label, 'nb tx')

    def test_total_recu_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('total_recu').verbose_name
        self.assertEquals(field_label, 'total recu')

    def test_total_envoye_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('total_envoye').verbose_name
        self.assertEquals(field_label, 'total envoye')

    def test_solde_final_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('solde_final').verbose_name
        self.assertEquals(field_label, 'solde final')

    def test_nb_bcalcules_utilisateur(self):
        u = Utilisateur.objects.get(adresse="test_adr")
        field_label = u._meta.get_field('nb_bcalcules').verbose_name
        self.assertEquals(field_label, 'nb bcalcules')

"""Test case utilisé pour tester les transactions models."""
class TransactionsModelTest(TestCase):
    @classmethod
    def setUp(self):
        Utilisateur.objects.create(adresse="test_adr",
                                   nb_tx=100,
                                   total_recu=300,
                                   total_envoye=200,
                                   solde_final=100,
                                   nb_bcalcules=100)
        u = Utilisateur.objects.get(adresse="test_adr")
        Transactions.objects.create(hash_tx = "test_hash_tx",
                                    date = 1583528848,
                                    hauteur = 600000,
                                    adresse = u
        )
    def test_hash_tx_transactions(self):
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")
        field_label = tx._meta.get_field('hash_tx').verbose_name
        self.assertEquals(field_label, 'hash tx')
        max_length = tx._meta.get_field('hash_tx').max_length
        self.assertEquals(max_length, 100)

    def test_date_transactions(self):
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")
        field_label = tx._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')
        max_length = tx._meta.get_field('date').max_length
        self.assertEquals(max_length, 20)

    def test_hauteur_transactions(self):
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")
        field_label = tx._meta.get_field('hauteur').verbose_name
        self.assertEquals(field_label, 'hauteur')

    def test_adresse_transactions(self):
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")
        field_label = tx._meta.get_field('adresse').verbose_name
        self.assertEquals(field_label, 'adresse')


"""Test case utilisé pour tester les inputs models."""
class InputsModelTest(TestCase):
    @classmethod
    def setUp(self):
        Utilisateur.objects.create(adresse="test_adr",
                                       nb_tx=100,
                                       total_recu=300,
                                       total_envoye=200,
                                       solde_final=100,
                                       nb_bcalcules=100)
        u = Utilisateur.objects.get(adresse="test_adr")

        Transactions.objects.create(hash_tx="test_hash_tx",
                                        date=1583528848,
                                        hauteur=600000,
                                        adresse=u
                                        )
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")

        Inputs.objects.create(
                adresse="test_adr",
                valeur_i="100.000",
                hash_tx=tx,
                date=1583528848
                                        )

    def test_adresse_inputs(self):
        i = Inputs.objects.get(adresse = "test_adr")
        field_label = i._meta.get_field('adresse').verbose_name
        self.assertEquals(field_label, 'adresse')
        max_length = i._meta.get_field('adresse').max_length
        self.assertEquals(max_length, 100)

    def test_valeur_i_inputs(self):
        i = Inputs.objects.get(adresse = "test_adr")
        field_label = i._meta.get_field('valeur_i').verbose_name
        self.assertEquals(field_label, 'valeur i')

    def test_hash_tx_inputs(self):
        i = Inputs.objects.get(adresse = "test_adr")
        field_label = i._meta.get_field('hash_tx').verbose_name
        self.assertEquals(field_label, 'hash tx')

    def test_date_inputs(self):
        i = Inputs.objects.get(adresse = "test_adr")
        field_label = i._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

"""Test case utilisé pour tester les inputs models."""
class OutputsModelTest(TestCase):
    @classmethod
    def setUp(self):
        Utilisateur.objects.create(adresse="test_adr",
                                       nb_tx=100,
                                       total_recu=300,
                                       total_envoye=200,
                                       solde_final=100,
                                       nb_bcalcules=100)
        u = Utilisateur.objects.get(adresse="test_adr")

        Transactions.objects.create(hash_tx="test_hash_tx",
                                        date=1583528848,
                                        hauteur=600000,
                                        adresse=u
                                        )
        tx = Transactions.objects.get(hash_tx = "test_hash_tx")

        Inputs.objects.create(
                adresse="test_adr",
                valeur_i="100.000",
                hash_tx=tx,
                date=1583528848)

    def test_adresse_outputs(self):
        o = Inputs.objects.get(adresse = "test_adr")
        field_label = o._meta.get_field('adresse').verbose_name
        self.assertEquals(field_label, 'adresse')
        max_length = o._meta.get_field('adresse').max_length
        self.assertEquals(max_length, 100)

    def test_valeur_i_outputs(self):
        o = Inputs.objects.get(adresse = "test_adr")
        field_label = o._meta.get_field('valeur_i').verbose_name
        self.assertEquals(field_label, 'valeur i')

    def test_hash_tx_outputs(self):
        o = Inputs.objects.get(adresse = "test_adr")
        field_label = o._meta.get_field('hash_tx').verbose_name
        self.assertEquals(field_label, 'hash tx')

    def test_date_outputs(self):
        o = Inputs.objects.get(adresse = "test_adr")
        field_label = o._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')