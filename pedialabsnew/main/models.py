from pagetree.reports import PagetreeReport, StandaloneReportColumn
from django.contrib.auth.models import User


class PedialabsReport(PagetreeReport):

    def users(self):
        users = User.objects.filter(
            is_superuser=True)
        return users.order_by('id')

    def standalone_columns(self):
        return [
            StandaloneReportColumn(
                "username", 'profile', 'string',
                'Unique Username', lambda x: x.username)]
