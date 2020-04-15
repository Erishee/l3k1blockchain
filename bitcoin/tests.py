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
from . import block
from django.conf import settings

# Create your tests here.

class Test_unitaire(TestCase):
    """Test case utilisé pour tester les fonctions de la classe Transaction de transacitons.py."""

    def test_convert_timestamps(self):
        """Test le fonctionnement de la fonction 'convert_timestamps'."""

        timestamps1 = 1586090057
        timestamps2 = 1515155657
        timestamps3 = 1474461257

        # Vérification
        self.assertEqual(Transaction.convert_timestamps(timestamps1), "2020-4-5")
        self.assertEqual(Transaction.convert_timestamps(timestamps2), "2018-1-5")
        self.assertEqual(Transaction.convert_timestamps(timestamps3), "2016-9-21")

    def test_get_current_time(self):
        """Test le fonctionnement de la fonction 'get_current_time'."""
        self.assertIsInstance(Transaction.get_current_time(), str)

    def test_get_current_price(self):
        """Test le fonctionnement de la fonction 'get_current_price'."""
        self.assertIsInstance(Transaction.get_current_price(), float)

    """Test case utilisé pour tester les fonctions de la classe Transaction de utilisateurs.py."""
    def test_stob(self):
        """Test le fonctionnement de la fonction 'stob'."""
        test_s1 = 111000000
        test_s2 = 1
        test_s3 = 0

        self.assertEqual(Utilisateurs.stob(test_s1), 1.11,)
        self.assertEqual(Utilisateurs.stob(test_s2), 0.00000001)
        self.assertEqual(Utilisateurs.stob(test_s3), 0)

    def test_btos(self):
        """Test le fonctionnement de la fonction 'btos'."""
        test_bt1 = 100000
        test_bt2 = 1.11
        test_bt3 = 0

        self.assertEqual(Utilisateurs.btos(test_bt1), 10000000000000)
        self.assertEqual(round(Utilisateurs.btos(test_bt2)), 111000000)
        self.assertEqual(Utilisateurs.btos(test_bt3), 0)

    def test_ftoi(self):
        """Test le fonctionnement de la fonction 'ftoi'."""
        test_f1 = 100001.99
        test_f2 = 1.11
        test_f3 = 0.99

        self.assertEqual(Utilisateurs.ftoi(test_f1), 100001)
        self.assertEqual(Utilisateurs.ftoi(test_f2), 1)
        self.assertEqual(Utilisateurs.ftoi(test_f3), 0)

    """Test case utilisé pour tester les fonctions de la classe Utilisateurs de utilisateur.py."""
    def test_max(self):
        """Tester le fonctionnement de la fonction 'max'."""
        user1= {
                    "adresse": "test_adr1",
                    "nb_tx": 111,
                    "total_recu": 111,
                    "total_envoye": 111,
                    "solde_final": 111,
                    "nb_balance": 111
        }
        user2 = {
                    "adresse": "test_adr2",
                    "nb_tx": 222,
                    "total_recu": 222,
                    "total_envoye": 222,
                    "solde_final": 222,
                    "nb_balance": 222
        }
        user3 = {
                    "adresse": "test_adr3",
                    "nb_tx": 333,
                    "total_recu": 333,
                    "total_envoye": 333,
                    "solde_final": 333,
                    "nb_balance": 333
        }
        list = []
        list.append(user1)
        list.append(user2)
        list.append(user3)
        usr = Utilisateurs.max(list)
        self.assertEqual("test_adr3", usr)

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



###############################################################
"""Test case utilisé pour tester les requête(ORM et CURSOR)."""
class Tester(TestCase):

    def setUp(self):
        fixtures = ['/bitcoin/fixtures/dump.json']

    def test_user(self):
        """Tester le fonctionnement de la fonction 'user'."""
        liste = Utilisateurs.dic_users()
        adr = Utilisateurs.max(liste)
        usr_rich_adr = Utilisateurs.user(adr)["adresse"]
        list_u = Utilisateur.objects.raw("SELECT adresse from utilisateur Order by solde_final")
        usr_rich_adrr = list_u[0].adresse
        self.assertEqual(usr_rich_adrr, usr_rich_adr)

    def test_get_all_tx(self):
        """Tester le fonctionnement de la fonction 'get_all_transaction'."""

        connection = psycopg2.connect(user="samtifshen",
                                      password="samtifshen",
                                      host="l3k1blockchain.caqj07wtufhq.us-east-1.rds.amazonaws.com",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        date_sql = "SELECT date FROM transactions Order by date"

        #cursor
        results_tx1 = cursor.execute(date_sql)

        #ORM
        results_tx2 = Transaction.get_all_tx()
        self.assertEqual(results_tx1, results_tx2)
