from datetime import datetime 
from bitcoin.utilisateurs import Utilisateurs
from bitcoin.models import Utilisateur
from bitcoin.models import Outputs 
from bitcoin.models import Inputs 
from bitcoin.models import Transactions



class Portefeuille:

	def __init__(self):
		self.date_inputs=[]
		self.valeur_i=[]

#methode permettant de récuperer les inputs d'un utilisateur (tout ce qu'il a envoyé)
#ainsi que la date à laquelle il a envoyé ses bitcoins  
	def get_inputs(self,adresse):
			inputs=Inputs.objects.raw("SELECT * from inputs WHERE adresse= %s ORDER BY date",[adresse])
			for i in inputs:
				self.date_inputs.append(datetime.fromtimestamp(i.date))
				self.valeur_i.append(Utilisateurs.stob(i.valeur_i))