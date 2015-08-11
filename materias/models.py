from django.db import models
from estudiantes.models import Estudiante
from decimal import Decimal

class Modulo(models.Model):
	nombre = models.CharField(max_length=25)

	def __unicode__(self):
		return self.nombre

class Materia(models.Model):
	sigla = models.CharField(max_length=10, primary_key=True)
	nombre = models.CharField(max_length=60)
	pre_requisito = models.ManyToManyField('Materia', blank=True, null=True)
	is_save_paralelo = models.BooleanField(default=False)
	modulo = models.ForeignKey(Modulo)
	record_academico = models.ManyToManyField(Estudiante, through='RecordAcademico')
	materias_inscritas = models.ManyToManyField(Estudiante, related_name='inscripcion')

	def __unicode__(self):
		return self.sigla + ' ' +self.nombre

class Paralelo(models.Model):
	nombre_docente = models.CharField(max_length=40)
	sigla_paralelo = models.CharField(max_length=1)
	id_materia = models.ForeignKey(Materia)

	def __unicode__(self):
		return self.id_materia.sigla + " " + self.sigla_paralelo

class Periodo(models.Model):
	dia = models.CharField(max_length=10)
	hora_inicio = models.TimeField(max_length=6)
	hora_final = models.TimeField(max_length=6)
	aula = models.CharField(max_length=25)
	id_paralelo = models.ForeignKey(Paralelo)

	def __unicode__(self):
		return '%s %s' % (self.id_paralelo.id_materia.sigla, self.aula)

class RecordAcademico(models.Model):
	estudiante = models.ForeignKey(Estudiante)
	materia = models.ForeignKey(Materia)
	sigla_paralelo = models.CharField(max_length=1, null=True, blank=True)
	nota = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
	gestion = models.CharField(max_length=6)

	def __unicode__(self):
		return '%s - %s' % (self.estudiante.name, self.materia.sigla)

	class Meta:
		unique_together = ("estudiante", "materia",)