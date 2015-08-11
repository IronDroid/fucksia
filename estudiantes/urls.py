from django.conf.urls import patterns, include, url

urlpatterns = patterns('estudiantes.views',
    url(r'^$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^perfil/$', 'perfil', name='perfil'),
    url(r'^record/$', 'record', name='record'),
    url(r'^record/recorrido/$', 'record_grafo', name='record_grafo'),
)
