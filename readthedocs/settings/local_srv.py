#coding=utf-8

from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rtd',
        'USER': 'rtd',
        'PASSWORD': 'rtd',
        'HOST': '',
        'PORT': '',
    }
}

DEBUG = False
TEMPLATE_DEBUG = False
CELERY_ALWAYS_EAGER = False

MEDIA_URL = 'http://media.docs-srv/'
STATIC_URL = 'http://media.docs-srv/static/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        # 'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        # 'URL': 'http://localhost:8983/solr',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'PREFIX': 'docs',
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

# Elasticsearch settings.
# ES_HOSTS = ['localhost:9200']
# ES_DEFAULT_NUM_REPLICAS = 1
# ES_DEFAULT_NUM_SHARDS = 5

SLUMBER_API_HOST = 'http://docs-srv'
WEBSOCKET_HOST = 'websocket.docs-srv:8088'

PRODUCTION_DOMAIN = 'docs-srv'
USE_SUBDOMAIN = True
NGINX_X_ACCEL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# Lock builds for 10 minutes
# REPO_LOCK_SECONDS = 300

try:
    from local_settings import *  # noqa
except ImportError:
    pass
