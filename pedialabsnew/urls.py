from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import pedialabsnew.main.views
import pedialabsnew.exercises.urls
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))

urlpatterns = patterns(
    '',
    auth_urls,
    (r'^registration/', include('registration.backends.default.urls')),
    (r'^$', 'pedialabsnew.main.views.index'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^exercises/', include(pedialabsnew.exercises.urls)),
    (r'^instructor/$', 'pedialabsnew.main.views.instructor_index'),
    (r'^instructor/(?P<uni>\w+)/lab/(?P<module_id>\d+)/$',
     'pedialabsnew.main.views.instructor_lab_report'),

    #Overview. The order of these routes are important:
    (r'^pages/public/edit/(?P<path>.*)$',
     pedialabsnew.main.views.EditPageOverview.as_view(),
     {}, 'edit-overview'),
    (r'^pages/public/(?P<path>.*)$',
     pedialabsnew.main.views.ViewPageOverview.as_view()),
    #Labs. The order of these routes are important:
    (r'^pages/labs/edit/(?P<path>.*)$',
     pedialabsnew.main.views.EditPage.as_view(),
     {}, 'edit-page'),
    (r'^pages/labs/instructor/(?P<path>.*)$',
     pedialabsnew.main.views.InstructorPage.as_view()),
    (r'^pages/labs/(?P<path>.*)$', pedialabsnew.main.views.ViewPage.as_view()),
)
