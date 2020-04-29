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

class Test_unitaire_db(TestCase):
    """Test case utilisé pour tester les fonctions qui a des interactions avec la bdd."""
    @classmethod
    def setUpTestData(self):
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
            Transactions.objects.create(hash_tx = "test_hash_tx4",
                                        date = "2018-10-20",
                                        hauteur = 600003,
                                        adresse = u3
            )
            Transactions.objects.create(hash_tx = "test_hash_tx5",
                                        date = "2018-10-20",
                                        hauteur = 600003,
                                        adresse = u3
            )
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
            tx1 = Transactions.objects.get(hash_tx="test_hash_tx1")
            tx2 = Transactions.objects.get(hash_tx="test_hash_tx2")
            tx3 = Transactions.objects.get(hash_tx="test_hash_tx3")
            tx4 = Transactions.objects.get(hash_tx="test_hash_tx4")
            tx5 = Transactions.objects.get(hash_tx="test_hash_tx5")

    def test_get_all_tx(self):
        tx=Transaction.get_all_tx()
        tx1 = Transactions.objects.get(hash_tx="test_hash_tx1")
        tx2 = Transactions.objects.get(hash_tx="test_hash_tx2")
        tx3 = Transactions.objects.get(hash_tx="test_hash_tx3")
        tx4 = Transactions.objects.get(hash_tx="test_hash_tx4")
        tx5 = Transactions.objects.get(hash_tx="test_hash_tx5")
        self.assertEqual(tx1, tx[0])
        self.assertEqual(tx2, tx[1])
        self.assertEqual(tx3, tx[2])
        self.assertEqual(len(tx), 5)

    def test_get_date_tx(self):
        tx=Transaction.get_all_tx()
        tx1 = Transactions.objects.get(hash_tx="test_hash_tx1")
        tx2 = Transactions.objects.get(hash_tx="test_hash_tx2")
        tx3 = Transactions.objects.get(hash_tx="test_hash_tx3")
        tx4 = Transactions.objects.get(hash_tx="test_hash_tx4")
        tx5 = Transactions.objects.get(hash_tx="test_hash_tx5")
        dict = Transaction.get_date_tx(tx)
        self.assertEqual(dict.get("2015-2-12"), 1)
        self.assertEqual(dict.get("2017-10-20"), 1)
        self.assertEqual(dict.get("2018-10-20"), 2)

    def test_biggest_users(self):
        u1 = Utilisateur.objects.get(adresse="test_adr1")
        u2 = Utilisateur.objects.get(adresse="test_adr2")
        u3 = Utilisateur.objects.get(adresse="test_adr3")

        users1 = Utilisateurs.biggest_users(0.0000005)
        users2 = Utilisateurs.biggest_users(0.000001)
        users3 = Utilisateurs.biggest_users(0.000002)
        all_usr = Utilisateur.objects.all()
        self.assertEqual(len(users1), len(all_usr))
        self.assertEqual(len(users2), 2)
        self.assertEqual(len(users3), 1)
        self.assertEqual(users3[0], all_usr[2])


    def test_dict_users(self):
        u1 = Utilisateur.objects.get(adresse="test_adr1")
        list_users = Utilisateurs.dic_users()
        self.assertEqual(len(list_users), 3)
        self.assertEqual(list_users[0].get("adresse"),u1.adresse )

    def test_user(self):
        u1 = Utilisateur.objects.get(adresse="test_adr1")
        list_user = Utilisateurs.user("test_adr1")
        self.assertEqual(list_user[0].get("adresse"),"test_adr1")
        self.assertEqual(list_user[0].get("solde_final"),Utilisateurs.stob(100))
        self.assertEqual(list_user[0].get("nb_tx"), 1)





