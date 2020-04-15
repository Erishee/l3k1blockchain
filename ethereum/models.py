# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Transactions(models.Model):
    hash_field = models.CharField(db_column='hash_', primary_key=True, max_length=300)  # Field renamed because it ended with '_'.
    timestamp_field = models.IntegerField(db_column='timestamp_', blank=True, null=True)  # Field renamed because it ended with '_'.
    block_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=300, blank=True, null=True)
    destination = models.CharField(max_length=300, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'


class Utilisateur(models.Model):
    address = models.CharField(primary_key=True, max_length=300)
    eth_balance = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisateur'
