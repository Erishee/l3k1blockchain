from django.shortcuts import render
from . import home
from blockchain import exchangerates
import ssl
import urllib, json
import urllib.request

# Create your views here.
def accueilBTC(request):
	ssl._create_default_https_context = ssl._create_unverified_context
	graphe = home.Accueil.afficherCours('BTC')
	ticker = exchangerates.get_ticker()
	prix_BTC = ticker['USD'].p15min
	return render(request, 'accueil/accueil.html', {'graphe_div':graphe, 'prix_BTC': prix_BTC})

def accueilETH(request):
	ssl._create_default_https_context = ssl._create_unverified_context
	url_price = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&api_key={7ca89d57703af8f97444c8d31f5df304306048b6475469cc70621b57d1927d16}"
	response = urllib.request.urlopen(url_price)
	current_price_json = json.loads(response.read())
	prix_ETH = current_price_json[u'USD']
	graphe = home.Accueil.afficherCours('ETH')
	return render(request, 'accueil/accueil.html', {'graphe_div':graphe,'prix_ETH': prix_ETH})