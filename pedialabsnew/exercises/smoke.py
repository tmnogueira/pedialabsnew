from smoketest import SmokeTest
from models import Lab


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        Lab.objects.all().count()
        self.assertTrue(True)
