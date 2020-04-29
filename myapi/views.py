from django.shortcuts import render
from rest_framework import viewsets
from bitcoin.models import Utilisateur, Bloc, Transactions, Inputs, Outputs
from .serializers import UtilisateurSerializer,BlocSerializer,TransactionsSerializer,InputsSerializer,OutputsSerializer
# Create your views here.

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by('solde_final')
    serializer_class = UtilisateurSerializer

class BlocViewSet(viewsets.ModelViewSet):
    queryset = Bloc.objects.all().order_by('hauteur')
    serializer_class = BlocSerializer

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all().order_by('date')
    serializer_class = TransactionsSerializer

class InputsViewSet(viewsets.ModelViewSet):
    queryset = Inputs.objects.all()[:5000]
    serializer_class = InputsSerializer

class OutputsViewSet(viewsets.ModelViewSet):
    queryset = Outputs.objects.all()[:5000]
    serializer_class = OutputsSerializer