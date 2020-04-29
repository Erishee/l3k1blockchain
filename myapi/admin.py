from django.contrib import admin
from bitcoin.models import Utilisateur, Bloc, Transactions
# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(Bloc)
admin.site.register(Transactions)