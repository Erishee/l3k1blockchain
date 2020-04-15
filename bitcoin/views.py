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
from bitcoin.portefeuille import Portefeuille
from . import block
import ssl
import pandas as pd



def bitcoin(request):
    seuil = 0
    liste_users = Utilisateur.objects.all()
    utilisateurs = Utilisateurs.biggest_users(seuil)
    users = Utilisateurs.dic_users()
    adresse = Utilisateurs.max(users)
    user = Utilisateurs.user(adresse)
    return render(request, 'bitcoin/bitcoin.html', {'utilisateurs': utilisateurs, 'user': user})


def portefeuille(request, adresse):
    utilisateurs = Utilisateurs.user(adresse)
    portefeuille = Portefeuille()
    portefeuille.get_inputs(adresse)
    x_data = portefeuille.date_inputs
    y_data = portefeuille.valeur_i
    plot_div = plot([Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')],
                    output_type='div')
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
    query = "SELECT adresse FROM utilisateur ORDER BY  nb_bcalcules DESC LIMIT 20"
    liste_adresses = Utilisateur.objects.raw(query)
    return render(request, 'bitcoin/blockchain_info.html', {'blocs' : blocs, 'top_20' : liste_adresses})


#méthode pour afficher toutes les transactions
#un schéma du cours et un graphe du nombre de transaction
def afficher_tx(request):

    #on recupere l'ensemble des transactions et l'adresse qui y est liée
    #puis on modifie le format de la date
    tx = Transaction.get_all_tx()

    current_time = Transaction.get_current_time()

    current_price = Transaction.get_current_price()
    #######
    #######plot cours_BTC
    #######
    # recuperer le cours du bitcoin de ce moment via l'url
    # en utilisant l'api du site cryptocompare

    # on recupere les données du fichier csv avec Pandas
    data = pd.read_csv('./static/DataVisualisation/csv/BTC_USD_2013-10-01_2020-03-28-CoinDesk.csv')
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
    context1 = {'fig_cours_BTC': fig_cours_BTC}

    Dict = Transaction.get_date_tx(tx)
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
        )
    )
    fig_tx_BTC = fig2.to_html(full_html=False)
    context2 = {'fig_tx_BTC': fig_tx_BTC}
    return render(request, 'bitcoin/transactions.html', {'results': tx,
                                                         'fig_cours_BTC': fig_cours_BTC,
                                                         'fig_tx_BTC': fig_tx_BTC,
                                                         'current_time':current_time,
                                                         'current_price':current_price})