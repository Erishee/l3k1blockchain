from django import forms 


class Seuil(forms.Form):
	seuil=forms.IntegerField(label="Veuillez inserer un seuil")
	date= forms.DateInput()