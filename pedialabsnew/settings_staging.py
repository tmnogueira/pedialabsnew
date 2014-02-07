# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/pedialabsnew/pedialabsnew/pedialabsnew/templates",
)

MEDIA_ROOT = '/var/www/pedialabsnew/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/pedialabsnew/pedialabsnew/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pedialabsnew',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/pedialabsnew/pedialabsnew/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

STATSD_PREFIX = 'pedialabsnew-staging'

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
