from smoketest import SmokeTest
from models import Lab


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Lab.objects.all().count()
        self.assertTrue(cnt > 0)
