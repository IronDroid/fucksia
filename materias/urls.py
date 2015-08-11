from django.conf.urls import patterns, include, url 

urlpatterns = patterns('materias.views',
    url(r'^horario/$', 'horario', name='horario'),
    url(r'^horario/materia/$', 'materia', name='materia'),
    url(r'^horario/inscripcion/$', 'inscripcion', name='inscripcion'),
)
