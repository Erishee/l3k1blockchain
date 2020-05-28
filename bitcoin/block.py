from bitcoin.models import Utilisateur, Bloc
import plotly.graph_objs as go
from plotly.offline import plot


class Block:

	#méthode qui calcule le nombre de blocs minés par une adresse
	#méthode qui s'applique à tous les blocs quand les compteurs sont à 0 
	@staticmethod
	def calcul_nb_bloc():
		#code fait pour être lancé juste apres l'ajout des blocs en masse
		"""
		liste_user = Utilisateur.objects.all() 
		for l in liste_user:
			l.nb_bcalcules = 0
			l.save()
		"""
		liste_blocs = Bloc.objects.all()
		for l in liste_blocs:
			user = Utilisateur.objects.get(adresse = l.adresse.adresse)
			user.nb_bcalcules += 1 
			user.save()

	#méthode qui retourne les 15 plus gros mineurs du bitcoin
	def get_top20():
		mineurs=[]
		nb_blocs=[]
		query="SELECT adresse,nb_bcalcules FROM utilisateur ORDER BY  nb_bcalcules DESC LIMIT 15"
		liste_adresses = Utilisateur.objects.raw(query)
		for a in liste_adresses:
			mineurs.append(a.adresse)
			nb_blocs.append(a.nb_bcalcules)
		return mineurs,nb_blocs

	#méthode qui fournit le diagramme circulaire des plus gros mineurs 	
	def plot_miners(mineurs,nb_blocs):
		fig = go.Figure(data=[go.Pie(labels=mineurs, values=nb_blocs)])
		fig.update_traces(hoverinfo='label+value', textinfo='value', textfont_size=15)
		plot_div = plot(fig, output_type='div', include_plotlyjs=False)
		return plot_div

	




