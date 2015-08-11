from django import forms
from django.forms import ModelForm
from .models import Estudiante

class EstudianteForm(ModelForm):
	name = forms.CharField(
		label='',
		widget=forms.TextInput(attrs={
			'class':'form-control',
            'placeholder':'Nombre de Usuario'}))
	email = forms.CharField(
		label='',
		widget=forms.TextInput(attrs={
			'class':'form-control',
            'placeholder':'Correo electronico'}))
	cod_estudiante = forms.CharField(
		label='',
		widget=forms.TextInput(attrs={
			'readonly':'readonly',
			'class':'form-control',
            'placeholder':'Codigo de estudiante'}))

	class Meta:
		model = Estudiante
		exclude = ('uid', 'avatar','social_network', 'social_url', 'is_config',)