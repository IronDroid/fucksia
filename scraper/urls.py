from django.conf.urls import patterns, include, url

urlpatterns = patterns('scraper.views',
    url(r'^config/$', 'config', name='config'),
    url(r'^update/$', 'update', name='update'),
    url(r'^admin/pensum/$', 'config_pensum', name='config_pensum'),
    url(r'^config/scraper/$', 'scraper', name='scraper'),
    url(r'^update/scraper/$', 'update_scraper', name='update_scraper'),
)
