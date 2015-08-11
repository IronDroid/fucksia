from django.db import models

from estudiantes.models import Estudiante
from materias.models import Materia

class Comentario(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    materia = models.ForeignKey(Materia)
    comentario = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comentario

class Respuesta(models.Model):
    comentario = models.ForeignKey(Comentario)
    respuesta = models.CharField(max_length=255)

    def __unicode__(self):
        return self.respuesta