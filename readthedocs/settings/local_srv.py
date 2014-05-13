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

DEBUG = False
TEMPLATE_DEBUG = False
CELERY_ALWAYS_EAGER = False

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ALWAYS_EAGER = False

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

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
SESSION_COOKIE_DOMAIN = 'localhost'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_DOMAIN = 'localhost'
CSRF_COOKIE_SECURE = False

SLUMBER_API_HOST = 'http://localhost:8000'

WEBSOCKET_HOST = 'localhost:8088'

IMPORT_EXTERNAL_DATA = False
DONT_HIT_DB = False
PRODUCTION_DOMAIN = 'localhost'
USE_SUBDOMAIN = True
NGINX_X_ACCEL_REDIRECT = True

# MEDIA_URL = 'https://media.readthedocs.org/'
# STATIC_URL = 'https://media.readthedocs.org/static/'
# ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://odin:8983/solr',
#     }
# }

# Elasticsearch settings.
# ES_HOSTS = ['backup:9200', 'db:9200']
# ES_DEFAULT_NUM_REPLICAS = 1
# ES_DEFAULT_NUM_SHARDS = 5

# Lock builds for 10 minutes
REPO_LOCK_SECONDS = 300

try:
    from local_settings import *  # noqa
except ImportError:
    pass
