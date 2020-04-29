import numpy as np
from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
import psycopg2
import datetime
import urllib, json
import urllib.request
import psycopg2
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



