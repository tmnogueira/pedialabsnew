from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': '/'})  # redirect_after_logout})

urlpatterns = patterns(
    '',
    auth_urls,
    #logout_page,
    (r'^registration/', include('registration.backends.default.urls')),
    (r'^$', 'pedialabsnew.main.views.index'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^logout/$',
     'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^pages/edit/(?P<path>.*)$', 'pedialabsnew.main.views.edit_page',
     {}, 'edit-page'),
    (r'^pages/instructor/(?P<path>.*)$',
     'pedialabsnew.main.views.instructor_page'),
    (r'^pages/(?P<path>.*)$', 'pedialabsnew.main.views.page'),

)
