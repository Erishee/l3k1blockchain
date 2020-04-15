from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('', views.bitcoin, name='bitcoin'),
    path('blockchain_info/', views.blockchain_info, name='blockchain_info'),
    path('transactions/', views.afficher_tx, name='transaction_info'),
    re_path(r'^portefeuille/(?P<adresse>\w+)/$',views.portefeuille,name='portefeuille'),
]