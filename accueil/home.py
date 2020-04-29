import pandas as pd
from plotly.offline import plot 
from plotly.graph_objs import Scatter
import pickle
from blockchain import blockexplorer, util
import math
import holoviews as hv 
from holoviews import opts, dim 
from bokeh.io import show
from bokeh.embed import file_html
from bokeh.resources import CDN
from datetime import datetime

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


	#liste des baleines les plus riches en bitcoins 
	top_10 = [	'1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF',
				'35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP', 
				'3KZ526NxCVXbKwwP66RgM3pte6zW4gY1tD', 
				'37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs', 
				'3M6UcBNGZAW1HRjiFDMRcY5aXFrQ4F9E1y',
				'3NnGcxybgm3drht65hRucr23Ya4ZmQqz4w',
				'386eAUqL3ZNZPmHeABXLo658DTQuJeLzUR',
				'3D8qAoMkZ8F1b42btt2Mn5TyN7sWfa434A',
				'1HQ3Go3ggs8pFnXuHVHRytPCq5fGG8Hbhx',
				'385cR5DM96n1HvBDMzLHPYcw89fZAXULJP',]

	#méthode qui converit la date de int (UNIX TIME) en string
	def convert_timestamps(t):
	    date = datetime.fromtimestamp(t)
	    if(date.month < 10):
	    	month = "0"+str(date.month)
	    else:
	    	month = str(date.month)
	    if(date.day < 10):
	    	day = "0"+str(date.day)
	    else:
	    	day = str(date.day)
	    new = str(date.year) + "-" + month + "-" + day
	    return new


	#methode qui permet de recupérer les objets Address des baleines via l'API blockchain
	def get_users():
		whales_address = list()
		for u in __class__.top_10:
			whales_address.append(blockexplorer.get_address(u))
		return whales_address


	#méthode qui permet de sérialiser les objets Address dans un fichier (plus rapide que les reqûetes via l'API)
	def serialize_users(whales_address):
		f = open('./static/serialize/whales_serialized', 'wb')
		pickle.dump(whales_address, f)


	#méthode qui permet de récupérer les objets Address qui ont été sérialisé
	def deserialize_users():
		f = open('./static/serialize/whales_serialized', 'rb')
		donnees = pickle.load(f)
		return donnees


	#methode permettant de récuperer les echanges entre les utilisateurs recupérés grace à deserialize_users()
	#chaque echange est stocké dans un tuple de la forme (source,destination,valeur)
	#whales_address: paramètre contenant les objets Address
	#retourne la liste de des echanges 
	def echanges(whales_address):
		echanges=[]
		for t in whales_address:
			transactions = t.transactions
			for tx in transactions:
				outputs = tx.outputs
				for u in __class__.top_10:
					if (u != t.address):
						for out in outputs:
							if(out.address == u):
								e = (t.address, out.address, out.value, __class__.convert_timestamps(tx.time))
								echanges.append(e)
		return echanges

	#methode qui permet de recuperer les echanges entre les utilisateurs
	#retourne la liste des echanges avec les index et non les adresses des utilisateurs
	def echanges_index(echanges):
		echanges_index = []
		for e in echanges:
			data = (__class__.top_10.index(e[0]), __class__.top_10.index(e[1]), e[2], e[3])
			echanges_index.append(data)
		return echanges_index


	#creation d'un dictionnaire contenant les liens et le noeuds du diagramme de chord 
	#echanges: echanges enttre les baleines 
	#retourne un dictionnaire des noeuds et des echanges
	def valeurs(echanges):
		data=dict()
		noeuds=[]
		liens=[]
		for u in __class__.top_10:
			n=dict()
			n['name']=u
			noeuds.append(n)
		for e in echanges:
			l=dict()
			l['source']=__class__.top_10.index(e[0])
			l['destination']=__class__.top_10.index(e[1])
			l['value']=math.floor(e[2])
			liens.append(l)
		for u in __class__.top_10:
			l=dict()
			l['source']=__class__.top_10.index(u)
			l['destination']=__class__.top_10.index(u)
			l['value']=e[2]
			liens.append(l)
		data['nodes']=noeuds
		data['links']=liens
		return data


	#methode permettant de construire le diagramme de chord 
	#parametre : dictionnaire contenant les liens et les noeuds 
	def chord(data):
		hv.extension('bokeh')
		renderer=hv.renderer('bokeh')
		hv.output(size=300)
		links= pd.DataFrame(data['links'])
		hv.Chord(links)
		nodes=hv.Dataset(pd.DataFrame(data['nodes']), 'index')
		chord=hv.Chord((links, nodes)).select(value=(10, None))
		chord.opts(
	    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), 
	               labels='name', node_color=dim('index').str()))
		bokeh_plot=renderer.get_plot(chord).state
		html=file_html(bokeh_plot,CDN,"my plot")
		return html
