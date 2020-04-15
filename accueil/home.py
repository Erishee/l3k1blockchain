import pandas as pd
from plotly.offline import plot 
from plotly.graph_objs import Scatter

class Accueil:

	@staticmethod
	def afficherCours(crypto):
		if(crypto == 'BTC'):
			data = pd.read_csv('./static/DataVisualisation/csv/BTC_USD_2013-10-01_2020-03-28-CoinDesk.csv')
		if(crypto == 'ETH'):
			data = pd.read_csv('./static/DataVisualisation/csv/ETH_USD_2015-08-09_2020-03-28-CoinDesk.csv')
		graphe = plot([Scatter(x=data['Date'],y=data['Closing Price (USD)'],
			mode='lines',name='test',opacity=0.8, marker_color='blue')],output_type='div')
		return graphe
