from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Lab, Test, TestResponse, ActionPlanResponse


class LabTest(TestCase):
    def test_add_form(self):
        f = Lab.add_form()
        self.assertTrue('description' in f.as_p())

    def test_needs_submit(self):
        lab = Lab.objects.create()
        self.assertTrue(lab.needs_submit())

    def test_redirect_to_self_on_submit(self):
        lab = Lab.objects.create()
        self.assertTrue(lab.redirect_to_self_on_submit())

    def test_edit_form(self):
        lab = Lab.objects.create()
        self.assertTrue("Situation urgent" in lab.edit_form().as_p())

    def test_add_test_form(self):
        lab = Lab.objects.create()
        self.assertTrue("normal_range" in lab.add_test_form().as_p())

    def test_all_abnormalities(self):
        lab = Lab.objects.create()
        self.assertTrue("Lymphocytosis" in lab.all_abnormalities())

    def test_unlocked(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        self.assertFalse(lab.unlocked(user))

    def test_submit_empty(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        lab.submit(user, dict())
        apr = ActionPlanResponse.objects.filter(user=user)
        self.assertEqual(apr.count(), 1)

    def test_submit_action_plan(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        lab.submit(
            user,
            {
                'action-plan': "panic!",
                'assessment': 'terminal'
            }
        )
        apr = ActionPlanResponse.objects.filter(user=user)
        self.assertEqual(apr.count(), 1)
        self.assertEqual(apr[0].action_plan, "panic!")
        self.assertEqual(apr[0].assessment, "terminal")

    def test_submit_with_results(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        t = Test.objects.create(lab=lab)
        lab.submit(
            user,
            {
                "result-%d" % t.id: "normal",
                "abnormality-%d" % t.id: "none",
            }
        )
        apr = ActionPlanResponse.objects.filter(user=user)
        self.assertEqual(apr.count(), 1)
        self.assertEqual(TestResponse.objects.all().count(), 1)


class TestTest(TestCase):
    def test_edit_form(self):
        lab = Lab.objects.create()
        t = Test.objects.create(lab=lab)
        f = t.edit_form()
        self.assertTrue("abnormality" in f.as_p())


class TestResponseTest(TestCase):
    def test_unicode(self):
        lab = Lab.objects.create()
        t = Test.objects.create(lab=lab)
        user = User.objects.create(username='test')
        tr = TestResponse.objects.create(test=t, user=user,
                                         result_level="normal")
        self.assertEqual(str(tr), 'TestResponse (Test object, test)')

    def test_correct_level(self):
        lab = Lab.objects.create()
        t = Test.objects.create(lab=lab)
        user = User.objects.create(username='test')
        tr = TestResponse.objects.create(test=t, user=user,
                                         result_level="normal")
        self.assertTrue(tr.correct_level())

    def test_correct_abnormality(self):
        lab = Lab.objects.create()
        t = Test.objects.create(lab=lab)
        user = User.objects.create(username='test')
        tr = TestResponse.objects.create(test=t, user=user,
                                         result_level="normal")
        self.assertTrue(tr.correct_abnormality())


class ActionPlanResponseTest(TestCase):
    def test_unicode(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        apr = ActionPlanResponse.objects.create(lab=lab, user=user)
        self.assertEqual(str(apr), 'ActionPlanResponse for test')

    def test_correct_action_plan(self):
        lab = Lab.objects.create()
        user = User.objects.create(username='test')
        apr = ActionPlanResponse.objects.create(lab=lab, user=user)
        self.assertTrue(apr.correct_action_plan())
