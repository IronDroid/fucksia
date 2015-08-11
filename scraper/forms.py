from django import forms

class PensumForm(forms.Form):
	pensum_URL = forms.URLField()
