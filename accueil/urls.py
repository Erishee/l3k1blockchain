from django.urls import path
from . import views

app_name='accueil'

urlpatterns = [
	path('', views.accueilBTC, name='accueil'),
    path('accueil_btc', views.accueilBTC, name='accueil_btc'),
    path('accueil_eth', views.accueilETH, name='accueil_eth'),
]