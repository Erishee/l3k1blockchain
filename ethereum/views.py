from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from datetime import datetime
from matplotlib import pyplot as plt
from ethereum.ethusers import EthUsers
from ethereum.models import Transactions
from ethereum.transactionETH import TransactionETH
from plotly.offline import plot 
import plotly.graph_objs as go 
from plotly.graph_objs import Scatter
import dash_html_components as html
import dash_core_components as dcc
from textwrap import dedent as d
from django_plotly_dash import DjangoDash
import dash
from bitcoin.RadarChart import RadarChart
import pandas as pd


def ethereum(request):
	utilisateurs=EthUsers.get_allusers()
	return render(request, 'ethereum/ethereum.html',{'utilisateurs':utilisateurs})

def portefeuille_eth(request,adresse):
	adresse=adresse
	year=[2010,2020]
	seuil=0
	user=EthUsers.get_user(adresse)
	x_data,y_data=EthUsers.get_transactions(adresse)
	fig=EthUsers.figure(x_data,y_data)	
	plot_div= plot(fig, output_type='div',include_plotlyjs=False)
	external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
	app=DjangoDash('connexions',external_stylesheets=external_stylesheets)
	app.layout = html.Div([
	    html.Div([html.H1("User's exchanges")],
	             style={'textAlign': "center",'font':'1em "Fira Sans", sans-serif'}),
	    html.Div(
	        children=[
	            html.Div(
	                children=[
	                    html.Div(
	                        children=[
	                            dcc.Markdown(d("""Choisissez un intervalle""")),
	                            dcc.RangeSlider(
	                                id='yearslider',
	                                min=2010,
	                                max=2020,
	                                step=1,
	                                value=[2010, 2020],
	                                marks={
	                                    2010: {'label': '2010'},
	                                    2011: {'label': '2011'},
	                                    2012: {'label': '2012'},
	                                    2013: {'label': '2013'},
	                                    2014: {'label': '2014'},
	                                    2015: {'label': '2015'},
	                                    2016: {'label': '2016'},
	                                    2017: {'label': '2017'},
	                                    2018: {'label': '2018'},
	                                    2019: {'label': '2019'},
	                                    2020: {'label': '2020'}
	                                    }
	                            ),
	                            html.Br(),
	                            html.Div(id='output-container-range-slider')
	                        ],
	                        style={'position':'absolute','height': '8%','width':'56%','colors':'#CDA277','float':'left','background':'#f0f0f0'}
	                    ),
	                    html.Div(
	                    children=[
	                        dcc.Markdown(d("""
	                        Choisissez un seuil
	                        """)),
	                        dcc.Input(id="valeurinp", type="number", placeholder="veuillez inserer un seuil"),
	                        html.Div(id="output")
	                        ],
	                        style={'position':'absolute','height': '8%','background':'#f0f0f0','float':'right','width':'39%','margin-left':'8%','display':'inline-block'}
	                    )
	                ],
	                style={'font':'caption','text-align':'center','margin-bottom':'2%'}
	            ),
	            html.Div(
	                children=[dcc.Graph(id="graphe",figure=EthUsers.star_graph(year, adresse,seuil))],
	                style={'width':'95%','border':'15px solid #f0f0f0','display':'inline-block','margin-top':'9%'}
	            )	                ]
	           )
	         ]
	       )

	@app.callback(
	    dash.dependencies.Output('graphe', 'figure'),
	    [dash.dependencies.Input('yearslider', 'value'),dash.dependencies.Input('valeurinp','value')])
	def update_output(value,valeurinp):
	    YEAR = value
	    SEUIL=valeurinp
	    return EthUsers.star_graph(value,adresse,valeurinp)
	return render(request, 'ethereum/portefeuille_eth.html',{'user':user,'plot_div':plot_div})


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
    Dict = TransactionETH.get_date_tx_eth(txs_eth)
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
    return render(request, 'ethereum/transactions_eth.html', {'txs_eth': txs_eth[len(txs_eth)-200:len(txs_eth)],
														 'fig_radar_chart': RadarChart.drawRadarChartETH(),
                                                         'fig_cours_ETH': fig_cours_ETH,
                                                         'fig_tx_ETH': fig_tx_ETH,
                                                         'Biggest_tx_24h_hash':RadarChart.eth_tx_hash_large24,
														 'Biggest_tx_24h_value': RadarChart.eth_tx_value_large24,})




