from ethereum.models import Transactions
import ssl
import urllib, json
import urllib.request
import datetime
from datetime import date
from datetime import datetime

class TransactionETH:

    #récupérer toutes les transactions par ORM ordonée par date
    @staticmethod
    def get_all_tx_eth():
        txs_eth = Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions_eth")
        return txs_eth

    #récupérer le temps de ce moment
    @staticmethod
    def get_current_time_eth():
        time_now = date.today()
        now = datetime.now()
        # dd/mm/YY H:M:S
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    #récupérer le cours BTC par l'API du site cryptocompare
    @staticmethod
    def get_current_price_eth():
        ssl._create_default_https_context = ssl._create_unverified_context
        # recuperer le cours du bitcoin de ce moment via l'url
        # en utilisant l'api du site cryptocompare
        url_price = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&api_key={7ca89d57703af8f97444c8d31f5df304306048b6475469cc70621b57d1927d16}"
        response = urllib.request.urlopen(url_price)
        current_price_json = json.loads(response.read())
        current_price = current_price_json[u'USD']
        return current_price

    #Méthode retourne un dictionnaire avec date la clé et nombre de fois la valeur.
    @staticmethod
    def get_date_tx_eth(transactions):
        Dict = {}
        for result in transactions:
            if result.timestamp_field not in Dict.keys():
                Dict[result.timestamp_field] = 1
            else:
                Dict[result.timestamp_field] += 1
        return Dict