from django.shortcuts import render
from . import home
from blockchain import exchangerates
import ssl
import urllib, json
import urllib.request
from ethereum.ethusers import EthUsers 

# Create your views here.
def accueilBTC(request):
	ssl._create_default_https_context = ssl._create_unverified_context
	graphe = home.Accueil.afficherCours('BTC')
	ticker = exchangerates.get_ticker()
	prix_BTC = ticker['USD'].p15min
	#whales_address = home.Accueil.get_users()
	#home.Accueil.serialize_users(whales_address)
	whales_address = home.Accueil.deserialize_users()
	echanges = home.Accueil.echanges(whales_address)
	echanges_index = home.Accueil.echanges_index(echanges)
	data = home.Accueil.valeurs(echanges)
	chord = home.Accueil.chord(data)
	return render(request, 'accueil/accueil.html', {'graphe_div':graphe, 'prix_BTC': prix_BTC, 'chord': chord, "echanges": echanges_index},)

def accueilETH(request):
	ssl._create_default_https_context = ssl._create_unverified_context
	url_price = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&api_key={7ca89d57703af8f97444c8d31f5df304306048b6475469cc70621b57d1927d16}"
	response = urllib.request.urlopen(url_price)
	current_price_json = json.loads(response.read())
	prix_ETH = current_price_json[u'USD']
	graphe = home.Accueil.afficherCours('ETH')
	utilisateurs=EthUsers.get_users()
	echanges=EthUsers.echanges(utilisateurs)
	data=EthUsers.valeurs(utilisateurs,echanges)
	chord_graph=EthUsers.chord(data)
	return render(request, 'accueil/accueil.html', {'graphe_div':graphe,'prix_ETH': prix_ETH,'chord_graph':chord_graph})