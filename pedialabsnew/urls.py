from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from pedialabsnew.main.views import EditPageOverview, ViewPageOverview, \
    EditPage, ViewPage, ClearStateView, InstructorPage, InstructorLabReport, \
    ReportView
import pedialabsnew.exercises.urls
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))

logout_page = (r'^accounts/logout/$',
               'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$',
                   'djangowind.views.logout',
                   {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
    (r'^registration/', include('registration.backends.default.urls')),
    (r'^$', 'pedialabsnew.main.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^_clear/$', ClearStateView.as_view()),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^exercises/', include(pedialabsnew.exercises.urls)),
    (r'^instructor/$', InstructorPage.as_view()),
    (r'^instructor/report/$', ReportView.as_view()),
    (r'^instructor/(?P<uni>\w+)/lab/(?P<module_id>\d+)/$',
     InstructorLabReport.as_view()),

    # Overview. The order of these routes are important:
    (r'^pages/public/edit/(?P<path>.*)$',
     EditPageOverview.as_view(), {}, 'edit-overview'),
    (r'^pages/public/(?P<path>.*)$', ViewPageOverview.as_view()),
    # Labs. The order of these routes are important:
    (r'^pages/labs/edit/(?P<path>.*)$', EditPage.as_view(), {}, 'edit-page'),
    (r'^pages/labs/(?P<path>.*)$', ViewPage.as_view()),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
