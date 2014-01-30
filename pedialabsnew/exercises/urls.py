from django.conf.urls import patterns

urlpatterns = patterns(
    'pedialabsnew.exercises.views',
    (r'^edit_lab/(?P<id>\d+)/$', 'edit_lab', {}, 'edit-lab'),
    (r'^edit_lab/(?P<id>\d+)/add_test/$',
     'add_test_to_lab', {}, 'add-test-to-lab'),
    (r'^edit_lab/(?P<id>\d+)/add_csv/$',
     'add_csv_to_lab', {}, 'add-csv-to-lab'),
    (r'^edit_test/(?P<id>\d+)/$', 'edit_test', {}, 'edit-test'),
    (r'^delete_test/(?P<id>\d+)/$', 'delete_test', {}, 'delete-test'),
    (r'^reorder_tests/(?P<id>\d+)/$', 'reorder_tests', {}, 'reorder-tests'),
)
