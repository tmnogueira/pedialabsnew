from django.test import TestCase
from django.test.client import Client
from ..models import Lab, Test


class ViewsTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_delete_test_get(self):
        l = Lab.objects.create()
        t = Test.objects.create(lab=l)
        r = self.c.get("/exercises/delete_test/%d/" % t.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue("<form" in r.content)

    def test_delete_test_post(self):
        l = Lab.objects.create()
        t = Test.objects.create(lab=l)
        r = self.c.post("/exercises/delete_test/%d/" % t.id, dict())
        self.assertEquals(r.status_code, 302)
        self.assertEquals(Test.objects.all().count(), 0)

    def test_reorder_tests(self):
        l = Lab.objects.create()
        t1 = Test.objects.create(lab=l, ordinality=1)
        t2 = Test.objects.create(lab=l, ordinality=2)
        r = self.c.post(
            "/exercises/reorder_tests/%d/" % l.id,
            {
                "test_1": t2.id,
                "test_2": t1.id,
            })
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.content, "ok")
