from django.db import models
from django.contrib.auth.models import User

class Estudiante(models.Model):
	uid = models.OneToOneField(User)
	name = models.CharField(max_length=100)
	email = models.EmailField(blank=True, null=True)
	avatar = models.URLField()
	social_network = models.CharField(max_length=20)
	social_url = models.URLField()
	cod_estudiante = models.CharField(max_length=10, blank=True)
	is_config = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name