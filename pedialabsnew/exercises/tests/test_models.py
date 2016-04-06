from django.contrib.auth.models import User
from django.test import TestCase
from ..models import (
    Lab, Test, TestResponse, ActionPlanResponse,
    TestLevelColumn, TestAbnormalityColumn,
    LabAssessmentColumn, LabActionPlanColumn,
)


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

    def test_edit(self):
        lab = Lab.objects.create()
        lab.edit({
            'description': 'new description',
            'assessment': True,
            'sickvisit': True,
        }, None)
        self.assertEqual(lab.description, 'new description')
        self.assertTrue(lab.assessment)
        self.assertTrue(lab.sickvisit)

    def test_update_tests_order(self):
        lab = Lab.objects.create()
        t1 = Test.objects.create(lab=lab)
        t2 = Test.objects.create(lab=lab)
        lab.update_tests_order([t2.id, t1.id])
        t1.refresh_from_db()
        t2.refresh_from_db()
        self.assertEqual(t2.ordinality, 1)
        self.assertEqual(t1.ordinality, 2)

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


class DummyHierarchy(object):
    id = 42
    name = 'dummy hierarchy'


class DummyTest(object):
    id = 23
    name = 'dummy test'


class TestTestLevelColumn(TestCase):
    def test_identifier(self):
        tlc = TestLevelColumn(DummyHierarchy(), DummyTest())
        self.assertEqual(tlc.identifier(), "42_23_level")

    def test_metadata(self):
        tlc = TestLevelColumn(DummyHierarchy(), DummyTest())
        self.assertEqual(
            tlc.metadata(),
            [
                'dummy hierarchy',
                "42_23_level",
                "Lab Result Level",
                "single choice",
                "dummy test",
                None,
            ])

    def test_user_value(self):
        tlc = TestLevelColumn(DummyHierarchy(), 4)
        user = User.objects.create(username='test')
        self.assertIsNone(tlc.user_value(user))


class TestTestAbnormalityColumn(TestCase):
    def test_identifier(self):
        tac = TestAbnormalityColumn(DummyHierarchy(), DummyTest())
        self.assertEqual(tac.identifier(), "42_23_abnormality")

    def test_metadata(self):
        tac = TestAbnormalityColumn(DummyHierarchy(), DummyTest())
        self.assertEqual(
            tac.metadata(),
            [
                'dummy hierarchy',
                "42_23_abnormality",
                "Lab Result Abnormality",
                "single choice",
                "dummy test",
                None,
            ])

    def test_user_value(self):
        tac = TestAbnormalityColumn(DummyHierarchy(), 4)
        user = User.objects.create(username='test')
        self.assertIsNone(tac.user_value(user))


class DummySection(object):
    label = "dummy section"


class DummyBlock(object):
    section = DummySection()


class DummyLab(object):
    id = 22

    def pageblock(self):
        return DummyBlock()


class TestLabAssessmentColumn(TestCase):
    def test_identifier(self):
        tlac = LabAssessmentColumn(DummyHierarchy(), DummyLab())
        self.assertEqual(tlac.identifier(), "42_22_assessment")

    def test_metadata(self):
        tlac = LabAssessmentColumn(DummyHierarchy(), DummyLab())
        self.assertEqual(
            tlac.metadata(),
            [
                'dummy hierarchy',
                "42_22_assessment",
                "Lab Assessment",
                "short text",
                "dummy section",
            ])

    def test_user_value(self):
        tlac = LabAssessmentColumn(DummyHierarchy(), 4)
        user = User.objects.create(username='test')
        self.assertIsNone(tlac.user_value(user))


class TestLabActionPlanColumn(TestCase):
    def test_identifier(self):
        tlapc = LabActionPlanColumn(DummyHierarchy(), DummyLab())
        self.assertEqual(tlapc.identifier(), "42_22_actionplan")

    def test_metadata(self):
        tlapc = LabActionPlanColumn(DummyHierarchy(), DummyLab())
        self.assertEqual(
            tlapc.metadata(),
            [
                'dummy hierarchy',
                "42_22_actionplan",
                "Lab Action Plan",
                "short text",
                "dummy section",
            ])

    def test_user_value(self):
        tlapc = LabActionPlanColumn(DummyHierarchy(), 4)
        user = User.objects.create(username='test')
        self.assertIsNone(tlapc.user_value(user))
