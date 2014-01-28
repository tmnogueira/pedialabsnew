from django.test import TestCase
from django.test.client import Client
from pagetree.helpers import get_hierarchy
from django.contrib.auth.models import User


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)
        assert "PASS" in response.content


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("labs", "/pages/labs/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })

    def test_page(self):
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_edit_page(self):
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/pages/labs/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("labs", "/pages/labs/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.superuser = User.objects.create(username="testsuperuser")
        self.superuser.set_password("test")
        self.superuser.is_superuser = True
        self.superuser.is_staff = True
        self.superuser.save()
        self.staff = User.objects.create(username="teststaff")
        self.staff.set_password("test")
        self.staff.is_staff = True
        self.staff.save()
        

    def test_page(self):
        self.c.login(username="testuser", password="test")
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)
        
        self.c.login(username="testsuperuser", password="test")
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)
        
        self.c.login(username="teststaff", password="test")
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        self.c.login(username="testuser", password="test")
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 302)

        self.c.login(username="testsuperuser", password="test")
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 200)

        self.c.login(username="teststaff", password="test")
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        self.c.login(username="testuser", password="test")
        r = self.c.get("/pages/labs/instructor/section-1/")
        self.assertEqual(r.status_code, 302)

        self.c.login(username="testsuperuser", password="test")
        r = self.c.get("/pages/labs/instructor/section-1/")
        self.assertEqual(r.status_code, 200)

        self.c.login(username="teststaff", password="test")
        r = self.c.get("/pages/labs/instructor/section-1/")
        self.assertEqual(r.status_code, 200)
