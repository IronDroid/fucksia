"""Development settings and globals."""


from os.path import join, normpath, dirname

from base import *

BASE_DIR = dirname(DJANGO_ROOT)

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fucksia',                      
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',                      
        'PORT': '5432',                      
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
# INSTALLED_APPS += (
#     'debug_toolbar',
# )

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': False,
#     'SHOW_TEMPLATE_CONTEXT': True,
# }
########## END TOOLBAR CONFIGURATION





SOCIAL_AUTH_FACEBOOK_KEY        = '950840118290987'
SOCIAL_AUTH_FACEBOOK_SECRET     = '27498946d8269ab43cb7acc09201753d'