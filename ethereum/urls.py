from django.urls import path,include,re_path
from . import views

app_name='ethereum'

urlpatterns = [
    path('', views.ethereum, name='ethereum'),
	path('transactions_eth/', views.afficher_tx_eth, name='afficher_tx_eth'),
    re_path(r'^portefeuille/(?P<adresse>\w+)/$',views.portefeuille_eth,name='portefeuille_eth'),

]