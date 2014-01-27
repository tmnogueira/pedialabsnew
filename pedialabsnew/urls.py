from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import PageView
import pedialabsnew.main.views
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
    #Overview:
    (r'^pages/public/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="public",
        hierarchy_base="/pages/public/")),
    (r'^pages/public/edit/(?P<path>.*)$', pedialabsnew.main.views.EditPageOverview.as_view(),
     {}, 'edit-page'),
    #Labs:
    (r'^pages/labs/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="labs",
        hierarchy_base="/pages/labs/")),
    (r'^pages/labs/edit/(?P<path>.*)$', pedialabsnew.main.views.EditPage.as_view(),
     {}, 'edit-page'),
    (r'^pages/labs/instructor/(?P<path>.*)$',
     pedialabsnew.main.views.InstructorPage.as_view()),

)