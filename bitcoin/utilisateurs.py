from bitcoin.models import Utilisateur
from bitcoin.models import Inputs
import math
from collections import OrderedDict 
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import datetime
import plotly.graph_objs as go


class Utilisateurs: 

# methode qui convertit les satoshis en btc 
	def stob(n):
		return n/100000000 

# methode qui convertit les satoshis en btc 
	def btos(n):
		return n*100000000

	def ftoi(n):
		return math.floor(n)

# méthode retournant une liste de  dictionnaire de tous les utilisateurs 
# elle permettra de recuperer le plus riche des utilisateurs 

	def dic_users():
		liste=[]
		query="SELECT * FROM utilisateur"
		utilisateur=Utilisateur.objects.raw(query)
		for u in utilisateur:
			d=dict()
			d["adresse"]=u.adresse
			d["nb_tx"]=u.nb_tx
			d["total_envoye"]=u.total_envoye
			d["total_recu"]=u.total_recu
			d["solde_final"]=u.solde_final
			liste.append(d)
			d=None 
		return liste 



# méthode retournant l'adresse de l'utilisateur possédant le plus de bitcoins 
# on regarde dans la liste celui qui possède le plus de bitcoins 

	def max(liste):
		adresse=""
		user=None 
		max_=Utilisateurs.stob(liste[0]["solde_final"]) 
		for li in liste[1:len(liste)]:
			if max_< Utilisateurs.stob(li["solde_final"]):
				user=li 
				max_=Utilisateurs.stob(li["solde_final"])
		adresse=user["adresse"]
		return adresse

#méthode retournant l'utilisateur possèdant le plus de bitcoins
#insère ses informations dans une liste

	def user(adresse):
		l=[]
		user=dict()
		a=adresse
		u=Utilisateur.objects.raw("SELECT * from utilisateur WHERE adresse = %s",[a])[0]
		user["adresse"]=u.adresse
		user["total_envoye"]= Utilisateurs.stob(u.total_envoye)
		user["total_recu"]=Utilisateurs.stob(u.total_recu)
		user["solde_final"]=Utilisateurs.stob(u.solde_final)
		user["nb_tx"]= u.nb_tx
		l.append(user)
		return l


#methode permettant de récuperer les inputs d'un utilisateur (tout ce qu'il a envoyé)
#ainsi que la date à laquelle il a envoyé ses bitcoins  
	def get_inputs(adresse):
		date_inputs=[]
		valeur_i=[]
		inputs=Inputs.objects.raw("SELECT * from inputs WHERE adresse= %s ORDER BY date",[adresse])
		for i in inputs:
			date_inputs.append(datetime.fromtimestamp(i.date))
			valeur_i.append(Utilisateurs.stob(i.valeur_i))
		return date_inputs,valeur_i

#méthode permettant de dessiner le graphe 
	def plot_inputs(dates,valeurs):
		fig=go.Figure()
		scatter=go.Scatter(x=dates, y=valeurs, mode='lines', name='test', opacity=0.8, marker_color='green')
		fig.add_trace(scatter)
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
		fig.update_layout(title="Btc sent over time",xaxis_title="Date",yaxis_title="BTC")
		plot_div=plot(fig,output_type='div')
		return plot_div

