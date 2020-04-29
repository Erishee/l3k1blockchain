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
from datetime import datetime
import csv
from datetime import date
from matplotlib import pyplot as plt
from ethereum.ethusers import EthUsers
from plotly.offline import plot 
import plotly.graph_objs as go 
from plotly.graph_objs import Scatter
import datetime
from datetime import datetime
import csv
from datetime import date

"""
from bitcoin.models import Utilisateur, Bloc, Transactions
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
from bitcoin.portefeuille import Portefeuille
"""
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
from ethereum.transactionETH import TransactionETH
import pandas as pd


def ethereum(request):
	utilisateurs=EthUsers.get_allusers()
	return render(request, 'ethereum/ethereum.html',{'utilisateurs':utilisateurs})

def portefeuille_eth(request,adresse):
	user=EthUsers.get_user(adresse)
	x_data=EthUsers.get_dates(adresse)
	y_data=EthUsers.get_transactions(adresse)
	#plot_div=plot([Scatter(x=x_data,y=y_data,mode='lines',name='test',opacity=0.8,marker_color='green')],output_type='div')
	fig=go.Figure(go.Scatter(x=x_data,y=y_data,mode='lines',name='test',opacity=0.8,marker_color='blue'))
	fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        	])
    	)
	)
	plot_div= plot(fig, output_type='div',include_plotlyjs=False)
	echanges=EthUsers.echanges(adresse)
	plot_div2=EthUsers.connexions(echanges,adresse)
	return render(request, 'ethereum/portefeuille_eth.html',{'user':user,'plot_div':plot_div,'plot_div2':plot_div2})


def afficher_tx_eth(request):

    #on recupere l'ensemble des informations des transactions ETH
    txs_eth = TransactionETH.get_all_tx_eth()

    current_time_eth = TransactionETH.get_current_time_eth()

    current_price_eth = TransactionETH.get_current_price_eth()

    #######
    #######plot cours_BTC
    #######
    # recuperer le cours du bitcoin de ce moment via l'url
    # en utilisant l'api du site cryptocompare

    # on recupere les données du fichier csv avec Pandas
    data = pd.read_csv('./static/DataVisualisation/csv/ETH_USD_2015-08-09_2020-03-28-CoinDesk.csv')
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(  x=data['Date'],
                                y=data['Closing Price (USD)'],
                                name="cours_ETH",
    ))
    fig1.layout.update( title="Ethereum Price",
                        xaxis_title="Date",
                        yaxis_title="Price($)",
                        font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
    ))
    fig_cours_ETH = fig1.to_html(full_html=False)
    context1 = {'fig_cours_ETH': fig_cours_ETH}

    Dict = TransactionETH.get_date_tx_eth(txs_eth)
    from_date = list(Dict.keys())[0]
    to_date = list(Dict.keys())[-1]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(  x=list(Dict.keys()),
                                y=list(Dict.values()),
                                name="tx_ETH",
    ))
    fig2.layout.update(
        title="Ethereum Transaciton By Date",
        xaxis_title="Date",
        yaxis_title="Transaction number",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig_tx_ETH = fig2.to_html(full_html=False)
    context2 = {'fig_tx_ETH': fig_tx_ETH}
    return render(request, 'ethereum/transactions_eth.html', {'txs_eth': txs_eth,
                                                         'fig_cours_ETH': fig_cours_ETH,
                                                         'fig_tx_ETH': fig_tx_ETH,
                                                         'current_time_eth':current_time_eth,
                                                         'current_price_eth':current_price_eth})


def top_utilisateurs_eth(request):
    return render(request, 'ethereum/top_utilisateurs_eth.html')
