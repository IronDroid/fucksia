from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('estudiantes.urls')),
    url(r'', include('timeline.urls')),
    url(r'', include('scraper.urls')),
    url(r'', include('generador.urls')),
    url(r'', include('materias.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)