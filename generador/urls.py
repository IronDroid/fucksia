from django.conf.urls import patterns, include, url

urlpatterns = patterns('generador.views',
    url(r'^generador/$', 'generador', name='generador'),
    url(r'^generador/generar/$', 'generar', name='generar'),
)
