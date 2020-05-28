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
import networkx as nx
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
from plotly.offline import plot 
import pandas as pd




class EthUsers:

#methode retournant la liste de tous les utilisateurs 

	def get_allusers():
		liste=[]
		utilisateurs=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur_eth")
		for u in utilisateurs:
			d=dict()
			d["adresse"]=u.address
			d["eth_balance"]=u.eth_balance
			liste.append(d)
		return liste


#methode permettant de recuperer un echantillon d'utilisateurs dans la bdd
#ces utilisateurs sont ceux possédant le plus d'ethereum

	def get_users():
		utilisateurs=[]
		result=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur_eth LIMIT 50")
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
			result=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions_eth WHERE source=%s",[u])
			for r in result:
				if r.destination in utilisateurs:
					e=(r.source,r.destination,r.value,r.timestamp_field)
					echanges.append(e)
		return echanges


	def echanges_index(echanges,utilisateurs):
		echanges_index=[]
		for e in echanges:
			r=(utilisateurs.index(e[0]),utilisateurs.index(e[1]),e[2],e[3])
			echanges_index.append(r)
		return echanges_index


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
		hv.output(size=230)
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

#retourne un utilisateur en fonction d'une adresse entré en paramètre 
	def get_user(adresse):
		l=[]
		user=dict()
		a=adresse
		u=Utilisateur.objects.db_manager('ethereum').raw("SELECT * from utilisateur_eth WHERE address = %s",[adresse])[0]
		user["adresse"]=u.address
		user["eth_balance"]=u.eth_balance
		l.append(user)
		return l

#paramètre: adresses -> adresse pour laquelle on souhaite recuperer les transactions 
#retour : liste -> liste des valeurs envoyés par l'utilisateur
#retour : dates -> dates auxquels cet utilisateur a envoyé 
	def get_transactions(adresse):
		liste=[]
		dates=[]
		transactions=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions_eth WHERE source = %s ORDER BY timestamp_",[adresse])
		for tx in transactions:
			liste.append(tx.value)
			dates.append(datetime.strptime(tx.timestamp_field,'%Y-%m-%d'))
		return dates,liste

#méthode permettant de construire le graphe du montant des echanges 
#param : dates -> liste de dates 
#		 transactions -> liste des valeurs envoyées 
	def figure(dates,transactions):
		fig=go.Figure(go.Scatter(x=dates,y=transactions,mode='lines',name='test',opacity=0.8,marker_color='blue'))
		fig.update_xaxes(rangeslider_visible=True,
    		rangeselector=dict(
        	buttons=list([
	            dict(count=1, label="1m", step="month", stepmode="backward"),
	            dict(count=6, label="6m", step="month", stepmode="backward"),
	            dict(count=1, label="YTD", step="year", stepmode="todate"),
	            dict(count=1, label="1y", step="year", stepmode="backward"),
	            dict(step="all")
        		])
    		),
		)
		fig.update_layout(xaxis_title="Date",yaxis_title="ETH")
		return fig 


#paramètre : adresse -> l'adresse pour laquelle on veut récuperer les echanges 
#retour : edge1 -> dictionnaire contenant les echanges d'un utilisateur 
#retour : nodes1 -> dictionnaire contenant tous les noeuds (utilisateurs avec qui adresse a echangé + adresse)
	def get_edges_nodes(adresse):
		edge1=dict()
		nodes1=dict()
		nodes=[]
		res1=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions_eth WHERE source=%s",[adresse])
		source=[]
		target=[]
		Datetime=[]
		TxAmt=[]
		for r in res1:
			if int(r.value)>0:
				source.append(r.source)
				target.append(r.destination)
				Datetime.append(datetime.strptime(r.timestamp_field,'%Y-%m-%d'))
				TxAmt.append(math.floor(r.value))
		res2=Transactions.objects.db_manager('ethereum').raw("SELECT * from transactions_eth WHERE destination=%s",[adresse])
		for r in res2:
			if int(r.value)>0:
				source.append(r.source)
				target.append(r.destination)
				Datetime.append(datetime.strptime(r.timestamp_field,'%Y-%m-%d'))
				TxAmt.append(math.floor(r.value))
		edge1['Source']=source
		edge1['Target']=target
		edge1['Datetime']=Datetime
		edge1['Value']=TxAmt
		nodes.extend(source)
		nodes.extend(target)
		n=list(set(nodes))
		nodes1['address']=n
		return edge1,nodes1

#methode permettant de construire le graphe en étoile des echanges 
#param : year -> liste contenant l'intervalle 
#        adresse -> adresse pour laquelle on souhaite visualiser les echanges 
#        seuil -> permet de filtrer les echanges en fonction d'un seuil 

	def star_graph(year,adresse,seuil):
		liens, noeuds= EthUsers.get_edges_nodes(adresse)
		edge1=pd.DataFrame(liens)
		node1=pd.DataFrame(noeuds)
		accountSet=set()
		for index in range(0,len(edge1)):
			if edge1['Datetime'][index].year<year[0] or edge1['Datetime'][index].year>year[1] or int(edge1['Value'][index])<seuil:
				edge1.drop(axis=0, index=index, inplace=True)
				continue
			accountSet.add(edge1['Source'][index])
			accountSet.add(edge1['Target'][index])

		users=[]
		centre=[]
		centre.append(adresse)
		users.append(centre)
		nds=[]
		for ele in accountSet:
			if ele!=adresse:
				nds.append(ele)
		users.append(nds)
		#centrer les utilisateurs autour d'un noeud 
		G = nx.from_pandas_edgelist(edge1, 'Source', 'Target', ['Source', 'Target', 'Value', 'Datetime'], create_using=nx.MultiDiGraph())
		if len(nds)>1:
			pos = nx.drawing.layout.shell_layout(G, users)
		else:
			pos = nx.drawing.layout.spring_layout(G)
		for node in G.nodes:
			G.nodes[node]['pos'] = list(pos[node])

		if len(nds)==0:
	 		data = []
	 		node_trace = go.Scatter(x=tuple([1]), y=tuple([1]), text=tuple([str(adresse)]), textposition="bottom center",
		                                mode='markers+text',
		                                marker={'size': 30, 'color': '#CDA277'})
	 		data.append(node_trace)
	 		node_trace1 = go.Scatter(x=tuple([1]), y=tuple([1]),
		                                mode='markers',
		                                marker={'size': 30, 'color': '#CDA277'},
		                                opacity=0)
	 		data.append(node_trace1)
	 		figure = {
	 			"data": data,
	 			"layout": go.Layout(title='', showlegend=False,
	 				margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
	 				xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
	 				yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
	 				height=600
	 				)}
	 		return figure
		
		data=[]
		for edge in G.edges:
			x0, y0 = G.nodes[edge[0]]['pos']
			x1, y1 = G.nodes[edge[1]]['pos']
			if math.floor(G.edges[edge]['Value'] / max(edge1['Value']) * 10)==0:
				weight=1
			else:
				weight =G.edges[edge]['Value'] / max(edge1['Value']) * 10
			trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
		                           mode='lines',
		                           line={'width': weight},
		                           marker={'color':'#A75C2E'},
		                           line_shape='spline',
		                           opacity=1)
			data.append(trace)
		node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
		 	                          hoverinfo="text", marker={'size': 30, 'color': '#CDA277'})
		for node in G.nodes():
			x, y = G.nodes[node]['pos']
			hovertext = "Adresse: " + str(node)
			text = node 
			node_trace['x'] += tuple([x])
			node_trace['y'] += tuple([y])
			node_trace['hovertext'] += tuple([hovertext])

		data.append(node_trace)
		middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers',
	                                    marker={'size': 20, 'color': 'LightSkyBlue'},
	                                    opacity=0)

		for edge in G.edges:
			x0, y0 = G.nodes[edge[0]]['pos']
			x1, y1 = G.nodes[edge[1]]['pos']
			hovertext = "From: " + str(G.edges[edge]['Source']) + "<br>" + "To: " + str(
		            G.edges[edge]['Target']) + "<br>" + "Value: " + str(
		            G.edges[edge]['Value']) + "<br>" + "TransactionDate: " + str(G.edges[edge]['Datetime'])
			middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
			middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
			middle_hover_trace['hovertext'] += tuple([hovertext])

		data.append(middle_hover_trace)
		figure = {
		        "data": data,
		        "layout": go.Layout(title='', showlegend=False, hovermode='closest',
		                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
		                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
		                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
		                            height=600,
		                            clickmode='event+select',
		                            annotations=[
		                                dict(
		                                    ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
		                                    ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
		                                    x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
		                                    y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
		                                    showarrow=True,
		                                    arrowhead=3,
		                                    arrowsize=4,
		                                    arrowwidth=1,
		                                    opacity=1
		                                ) for edge in G.edges]
		                            )}
		return figure


