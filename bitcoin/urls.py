from django.urls import path,include,re_path
from . import views

app_name='bitcoin'

urlpatterns = [
    path('', views.bitcoin, name='bitcoin'),
    path('blockchain_info/', views.blockchain_info, name='blockchain_info'),
    path('transactions/', views.afficher_tx, name='afficher_tx'),
    re_path(r'^portefeuille/(?P<adresse>\w+)/$',views.portefeuille,name='portefeuille'),
]