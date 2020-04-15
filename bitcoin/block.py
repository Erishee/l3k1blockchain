from bitcoin.models import Utilisateur, Bloc

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
	




