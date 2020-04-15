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
from matplotlib import pyplot as plt
from ethereum.ethusers import EthUsers
from plotly.offline import plot 
import plotly.graph_objs as go 
from plotly.graph_objs import Scatter
"""
from bitcoin.models import Utilisateur, Bloc, Transactions
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.transactions import Transaction
from bitcoin.portefeuille import Portefeuille
"""
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter


def ethereum(request):
	utilisateurs=EthUsers.get_allusers()
	return render(request, 'ethereum/ethereum.html',{'utilisateurs':utilisateurs})

def portefeuille_eth(request,adresse):
	user=EthUsers.get_user(adresse)
	x_data=EthUsers.get_dates(adresse)
	y_data=EthUsers.get_transactions(adresse)
	plot_div=plot([Scatter(x=x_data,y=y_data,mode='lines',name='test',opacity=0.8,marker_color='green')],output_type='div')
	return render(request, 'ethereum/portefeuille_eth.html',{'user':user,'plot_div':plot_div})


def afficher_tx_eth(request):
    return render(request, 'ethereum/transactions_eth.html')

def top_utilisateurs_eth(request):
    return render(request, 'ethereum/top_utilisateurs_eth.html')
