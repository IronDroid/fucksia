from django.conf.urls import patterns, include, url

urlpatterns = patterns('timeline.views',
    url(r'^home/$', 'home', name='home'),

    url(r'^home/guardar-comentario/$', 'guardar_comentario', name='guardar_comentario'),
    url(r'^home/cargar-respuestas/(?P<id>\d+)$', 'cargar_respuestas', name='cargar_respuestas'),
    url(r'^guardar-respuesta/$', 'guardar_respuesta', name='guardar_respuesta'),
    url(r'^conocidos/$', 'conocidos', name='conocidos'),
)
