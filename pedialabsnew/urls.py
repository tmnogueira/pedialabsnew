import django.contrib.auth.views
import django.views.static
import djangowind.views
import pedialabsnew.exercises.urls

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from pedialabsnew.main.views import EditPageOverview, ViewPageOverview, \
    EditPage, ViewPage, ClearStateView, InstructorPage, InstructorLabReport, \
    ReportView, index

admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))

logout_page = url(r'^accounts/logout/$',
                  django.contrib.auth.views.logout,
                  {'next_page': redirect_after_logout})
admin_logout_page = url(r'^accounts/logout/$',
                        django.contrib.auth.views.logout,
                        {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(r'^accounts/logout/$',
                      djangowind.views.logout,
                      {'next_page': redirect_after_logout})
    admin_logout_page = url(r'^admin/logout/$',
                            djangowind.views.logout,
                            {'next_page': redirect_after_logout})

urlpatterns = [
    logout_page,
    admin_logout_page,
    auth_urls,
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^_clear/$', ClearStateView.as_view()),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^quizblock/', include('quizblock.urls')),
    url(r'^exercises/', include(pedialabsnew.exercises.urls)),
    url(r'^instructor/$', InstructorPage.as_view()),
    url(r'^instructor/report/$', ReportView.as_view()),
    url(r'^instructor/(?P<uni>\w+)/lab/(?P<module_id>\d+)/$',
        InstructorLabReport.as_view()),

    # Overview. The order of these routes are important:
    url(r'^pages/public/edit/(?P<path>.*)$',
        EditPageOverview.as_view(), {}, 'edit-overview'),
    url(r'^pages/public/(?P<path>.*)$', ViewPageOverview.as_view()),
    # Labs. The order of these routes are important:
    url(r'^pages/labs/edit/(?P<path>.*)$', EditPage.as_view(), {},
        'edit-page'),
    url(r'^pages/labs/(?P<path>.*)$', ViewPage.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
