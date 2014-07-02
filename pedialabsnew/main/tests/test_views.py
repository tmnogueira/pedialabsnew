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
        r = self.c.get("/instructor/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedInUser(TestCase):
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
        self.c.login(username="testuser", password="test")

    def test_page(self):
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/instructor/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_labreport(self):
        section = self.root.get_descendants()[0]
        url = '/instructor/%s/lab/%s/' % (self.u.username, section.id)
        r = self.c.get(url)
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedInSuperUser(TestCase):
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
        self.superuser = User.objects.create(username="testsuperuser")
        self.superuser.set_password("test")
        self.superuser.is_superuser = True
        self.superuser.is_staff = True
        self.superuser.save()
        self.c.login(username="testsuperuser", password="test")

    def test_page(self):
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.c.get("/instructor/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_labreport(self):
        section = self.root.get_descendants()[0]
        url = '/instructor/%s/lab/%s/' % (self.superuser.username, section.id)
        r = self.c.get(url)
        self.assertEqual(r.status_code, 200)


class PagetreeViewTestsLoggedInStaff(TestCase):
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
        self.staff = User.objects.create(username="teststaff")
        self.staff.set_password("test")
        self.staff.is_staff = True
        self.staff.save()
        self.c.login(username="teststaff", password="test")

    def test_page(self):
        r = self.c.get("/pages/labs/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/labs/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/instructor/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_labreport(self):
        section = self.root.get_descendants()[0]
        url = '/instructor/%s/lab/%s/' % (self.staff.username, section.id)
        r = self.c.get(url)
        self.assertEqual(r.status_code, 200)
