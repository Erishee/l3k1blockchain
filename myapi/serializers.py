from rest_framework import serializers
from bitcoin.models import Utilisateur, Bloc, Transactions, Inputs, Outputs

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields =('adresse','nb_tx','total_recu','total_envoye','solde_final','nb_bcalcules')

class BlocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloc
        fields =('hauteur','hash_bloc','adresse','nb_tx')

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields =('hash_tx','date','hauteur','adresse')

class InputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inputs
        fields =('adresse','valeur_i','hash_tx','date')

class OutputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outputs
        fields =('adresse','valeur_i','hash_tx','date')