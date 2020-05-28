import numpy as np
from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
import psycopg2
import datetime
import urllib, json
import urllib.request
import datetime
from datetime import datetime
import csv
from datetime import date
from matplotlib import pyplot as plt
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from bitcoin.models import Transactions
import ssl
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter



class Transaction:

    #méthode pour convertir le timestamps en temps réel
    @staticmethod
    def convert_timestamps(t):
        date = datetime.fromtimestamp(t)
        new = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        return new

    #récupérer toutes les transactions par ORM ordonée par date
    @staticmethod
    def get_all_tx():
        tx = Transactions.objects.all().order_by('date').select_related('adresse')
        return tx

    #récupérer le temps de ce moment
    @staticmethod
    def get_current_time():
        time_now = date.today()
        now = datetime.now()
        # dd/mm/YY H:M:S
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    #récupérer le cours BTC par l'API du site cryptocompare
    @staticmethod
    def get_current_price():
        ssl._create_default_https_context = ssl._create_unverified_context
        # recuperer le cours du bitcoin de ce moment via l'url
        # en utilisant l'api du site cryptocompare
        url_price = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key={7ca89d57703af8f97444c8d31f5df304306048b6475469cc70621b57d1927d16}"
        response = urllib.request.urlopen(url_price)
        current_price_json = json.loads(response.read())
        current_price = current_price_json[u'USD']
        return current_price

    #Méthode retourne un dictionnaire avec date la clé et nombre de fois la valeur.
    @staticmethod
    def get_date_tx(transactions):
        Dict = {}
        for result in transactions:
            if result.date not in Dict.keys():
                Dict[result.date] = 1
            else:
                Dict[result.date] += 1
        return Dict

#methode permettant d'afficher le cours du btc sur un graphe 
    def fig_cours_BTC(data):
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(  x=data['Date'],
                                y=data['Closing Price (USD)'],
                                name="cours_BTC",
                                ))
        fig1.layout.update( title="Bitcoin Price",
                        xaxis_title="Date",
                        yaxis_title="Price($)",
                        font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                        ))
        fig_cours_BTC = fig1.to_html(full_html=False)
        return fig_cours_BTC

#methode permettant d'afficher les transactions sur un graphe 
    def fig_tx_BTC(Dict):
        from_date = list(Dict.keys())[0]
        to_date = list(Dict.keys())[-1]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(  x=list(Dict.keys()),
                                y=list(Dict.values()),
                                name="tx_BTC",
                                ))
        fig2.layout.update(
            title="Bitcoin Transaciton By Date",
            xaxis_title="Date",
            yaxis_title="Transaction number",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
                ))
        fig_tx_BTC = fig2.to_html(full_html=False)
        return fig_tx_BTC




