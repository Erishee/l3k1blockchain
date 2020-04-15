from bitcoin.models import Utilisateur
import math
from collections import OrderedDict 

class Utilisateurs: 

# methode qui convertit les satoshis en btc 
	def stob(n):
		return n/100000000 

# methode qui convertit les satoshis en btc 
	def btos(n):
		return n*100000000

	def ftoi(n):
		return math.floor(n)

# méthode permettant de recuperer les plus gros utilisateurs de bitcoins 
# prend en paramètre le seuil 
# retourne un tableau contenant les utilisateurs possédant plus de n bitcoins 

	def biggest_users(n):
		n=Utilisateurs.btos(n)
		query='SELECT * FROM utilisateur WHERE solde_final > %s'%n
		utilisateurs=Utilisateur.objects.raw(query)
		return utilisateurs

# méthode retournant une liste de  dictionnaire de tous les utilisateurs 
# elle permettra de recuperer le plus riche des utilisateurs 

	def dic_users():
		liste=[]
		query="SELECT * FROM utilisateur"
		utilisateur=Utilisateur.objects.raw(query)
		for u in utilisateur:
			d=dict()
			d["adresse"]=u.adresse
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