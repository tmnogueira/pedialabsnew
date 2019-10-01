from pedialabsnew.exercises.models import Lab
from smoketest import SmokeTest


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        Lab.objects.all().count()
        self.assertTrue(True)
