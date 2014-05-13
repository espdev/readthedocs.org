#coding=utf-8

from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docs',
        'USER': 'docs',
        'PASSWORD': 'docs',
        'HOST': '',
        'PORT': '',
    }
}

# DEBUG = False
# TEMPLATE_DEBUG = False

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_HTTPONLY = False
CACHE_BACKEND = 'dummy://'

SLUMBER_API_HOST = 'http://localhost:8000'
PRODUCTION_DOMAIN = 'localhost:8000'

WEBSOCKET_HOST = 'localhost:8088'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

IMPORT_EXTERNAL_DATA = False
DONT_HIT_DB = False
NGINX_X_ACCEL_REDIRECT = True

CELERY_ALWAYS_EAGER = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For testing locally. Put this in your /etc/hosts:
# 127.0.0.1 test
# and navigate to http://test:8000
CORS_ORIGIN_WHITELIST = (
    'test:8000',
)

try:
    from local_settings import *  # noqa
except ImportError:
    pass
