from django.urls import path
from . import views

urlpatterns = [
	path('', views.accueilBTC, name='accueil'),
    path('accueil_btc', views.accueilBTC, name='accueil'),
    path('accueil_eth', views.accueilETH, name='accueil'),
]