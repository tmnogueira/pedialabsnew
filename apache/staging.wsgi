import os, sys, site

site.addsitedir('/var/www/pedialabsnew/pedialabsnew/ve/lib/python2.7/site-packages')
sys.path.append('/var/www/pedialabsnew/pedialabsnew/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pedialabsnew.settings_staging'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
