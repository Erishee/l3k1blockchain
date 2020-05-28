from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
import psycopg2
import datetime
import urllib, json
import urllib.request
import psycopg2
import datetime
from datetime import datetime
import csv
from datetime import date
import plotly.offline as opy
from django.views.generic import TemplateView
from matplotlib import pyplot as plt
from bitcoin.models import Utilisateur, Bloc, Transactions
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
from . import block
import ssl
import pandas as pd
from bitcoin.block import Block
from bitcoin.RadarChart import RadarChart



def bitcoin(request):
    liste_users = Utilisateur.objects.all()
    users = Utilisateurs.dic_users()
    adresse = Utilisateurs.max(users)
    user = Utilisateurs.user(adresse)
    return render(request, 'bitcoin/bitcoin.html', {'utilisateurs': users, 'user': user})


def portefeuille(request, adresse):
    utilisateurs = Utilisateurs.user(adresse)
    x_data,y_data = Utilisateurs.get_inputs(adresse)
    plot_div = Utilisateurs.plot_inputs(x_data,y_data)
    return render(request, 'bitcoin/portefeuille.html', {'utilisateurs': utilisateurs, 'plot_div': plot_div})



def blockchain_info(request):
    blocs = Bloc.objects.all().select_related('adresse')
    for b in blocs:
        hash = b.hash_bloc
        while(hash.startswith('0')):
            hash=hash[1:]
        hash = "00...0"+hash
        b.hash_bloc = hash
    #block.Block.calcul_nb_bloc() fonction marche 
    #mais pas nécéssaire de la lancer à chaque fois tant qu'on a pas tous les blocs
    mineurs,nb_blocs=Block.get_top20()
    plot_div=Block.plot_miners(mineurs,nb_blocs)
    return render(request, 'bitcoin/blockchain_info.html', {'blocs' : blocs, 'plot_div' : plot_div})


#méthode pour afficher toutes les transactions
#un schéma du cours et un graphe du nombre de transaction
def afficher_tx(request):

    #on recupere l'ensemble des transactions et l'adresse qui y est liée
    #puis on modifie le format de la date
    tx = Transactions.objects.all().order_by('date').select_related('adresse')
    current_time = Transaction.get_current_time()
    current_price = Transaction.get_current_price()
    #######plot cours_BTC
    # recuperer le cours du bitcoin de ce moment via l'url
    # en utilisant l'api du site cryptocompare
    # on recupere les données du fichier csv avec Pandas
    data = pd.read_csv('./static/DataVisualisation/csv/BTC_USD_2013-10-01_2020-03-28-CoinDesk.csv')
    fig_cours_BTC=Transaction.fig_cours_BTC(data)
    #######plot radar chart
    fig_radar_chart = RadarChart.drawRadarChart()

    Dict = Transaction.get_date_tx(tx)
    fig_tx_BTC=Transaction.fig_tx_BTC(Dict)
    return render(request, 'bitcoin/transactions.html', {'results': tx[len(tx)-200:len(tx)],
                                                         'fig_radar_chart': fig_radar_chart,
                                                         'fig_cours_BTC': fig_cours_BTC,
                                                         'fig_tx_BTC': fig_tx_BTC,
                                                         'Biggest_tx_24h_hash': RadarChart.btc_tx_hash_large24,
                                                         'Biggest_tx_24h_value': RadarChart.btc_tx_value_large24})