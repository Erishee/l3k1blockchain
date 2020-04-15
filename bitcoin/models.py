from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


# Chaque classe représente une table de la base de données 

class Bloc(models.Model):
    hauteur = models.IntegerField(primary_key=True)
    hash_bloc = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='adresse', blank=True, null=True)
    nb_tx = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bloc'


class Inputs(models.Model):
    adresse = models.CharField(primary_key=True, max_length=100)
    valeur_i = models.FloatField()
    hash_tx = models.ForeignKey('Transactions', models.DO_NOTHING, db_column='hash_tx')
    date = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'inputs'
        unique_together = (('adresse', 'valeur_i', 'hash_tx', 'date'),)


class Outputs(models.Model):
    adresse = models.CharField(primary_key=True, max_length=100)
    valeur_i = models.FloatField()
    hash_tx = models.ForeignKey('Transactions', models.DO_NOTHING, db_column='hash_tx')
    date = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'outputs'
        unique_together = (('adresse', 'valeur_i', 'hash_tx', 'date'),)


class Transactions(models.Model):
    hash_tx = models.CharField(primary_key=True, max_length=100)
    date = models.CharField(max_length=20, blank=True, null=True)
    hauteur = models.IntegerField(blank=True, null=True)
    adresse = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='adresse', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'transactions'


class Utilisateur(models.Model):
    adresse = models.CharField(primary_key=True, max_length=100)
    nb_tx = models.IntegerField(blank=True, null=True)
    total_recu = models.FloatField(blank=True, null=True)
    total_envoye = models.FloatField(blank=True, null=True)
    solde_final = models.FloatField(blank=True, null=True)
    nb_bcalcules = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'utilisateur'

