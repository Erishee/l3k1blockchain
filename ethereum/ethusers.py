from ethereum.models import Utilisateur
from ethereum.models import Transactions 
from datetime import datetime
import math
import pandas as pd 
import holoviews as hv 
from holoviews import opts, dim 
from bokeh.io import show
from bokeh.embed import file_html
from bokeh.resources import CDN

class EthUsers:

#methode retournant la liste de tous les utilisateurs 

	def get_allusers():
		liste=[]
		utilisateurs=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur")
		for u in utilisateurs:
			d=dict()
			d["adresse"]=u.address
			d["eth_balance"]=u.eth_balance
			liste.append(d)
		return liste


#methode permettant de recuperer un echantillon de 200 utilisateurs dans la bdd
#ces 200 utilisateurs sont ceux possédant le plus d'ethereum

	def get_users():
		utilisateurs=[]
		result=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur LIMIT 200")
		for r in result:
			utilisateurs.append(r.address)
		return utilisateurs

#methode permettant de récuperer les echanges entre les utilisateurs recupérés grace à get_users()
#chaque echange est stocké dans un tuple de la forme (source,destination,valeur)
#utilisateur: paramètre contenant la liste des utilisateurs 
#retourne la liste de des echanges 

	def echanges(utilisateurs):
		echanges=[]
		for u in utilisateurs:
			result=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions WHERE source=%s",[u])
			for r in result:
				if r.destination in utilisateurs:
					e=(r.source,r.destination,r.value)
					echanges.append(e)
		return echanges

#creation d'un dictionnaire contenant les liens et le noeuds du diagramme de chord 
#utilisateurs: utilisateurs recupérés 
#echanges: echanges enttre ces utilisateurs 
#retourne un dictionnaire des noeuds et des echanges
	def valeurs(utilisateurs,echanges):
		data=dict()
		noeuds=[]
		liens=[]
		for u in utilisateurs:
			n=dict()
			n['name']=u
			noeuds.append(n)
		for e in echanges:
			l=dict()
			l['source']=utilisateurs.index(e[0])
			l['destination']=utilisateurs.index(e[1])
			l['value']=math.floor(e[2])
			liens.append(l)
		data['nodes']=noeuds
		data['links']=liens 
		return data 

#methode permettant de construire le diagramme de chord 
#parametre : dictionnaire contenant les liens et les noeuds 
	def chord(data):
		hv.extension('bokeh')
		renderer=hv.renderer('bokeh')
		hv.output(size=200)
		links=pd.DataFrame(data['links'])
		hv.Chord(links)
		nodes=hv.Dataset(pd.DataFrame(data['nodes']), 'index')
		chord=hv.Chord((links, nodes)).select(value=(10, None))
		chord.opts(
	    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), 
	               labels='name', node_color=dim('index').str()))
		bokeh_plot=renderer.get_plot(chord).state
		html=file_html(bokeh_plot,CDN,"my plot")
		return html 


	def get_user(adresse):
		l=[]
		user=dict()
		a=adresse
		u=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur WHERE address = %s",[adresse])[0]
		user["adresse"]=u.address
		user["eth_balance"]=u.eth_balance
		l.append(user)
		return l


	def get_transactions(adresse):
		liste=[]
		transactions=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions WHERE source = %s ORDER BY timestamp_",[adresse])
		for tx in transactions:
			liste.append(tx.value)
		return liste 

	def get_dates(adresse):
		liste=[]
		dates=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions WHERE source = %s ORDER BY timestamp_",[adresse])
		for d in dates:
			liste.append(datetime.fromtimestamp(d.timestamp_field))
		return liste 


