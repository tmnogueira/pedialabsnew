from django.db import models
from pagetree.models import PageBlock
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django import forms
from django.core.urlresolvers import reverse


class Lab(models.Model):
    description = models.TextField(blank=True)
    assessment = models.BooleanField(default=False)
    sickvisit = models.BooleanField(default=False)
    correct_actionplan = models.CharField(
        max_length=256,
        default="",
        choices=[("Situation urgent. Call or admit patient immediately",
                  "Situation urgent. Call or admit patient immediately"),
                 ("Situation needs follow-up. Call patient within a week",
                  "Situation needs follow-up. Call patient within a week"),
                 ("Flag for review at following visit",
                  "Flag for review at following visit"),
                 ("Call patient's mother to say the results were normal",
                  "Call patient's mother to say the results were normal"),
                 ("Prescribe treatment", "Prescribe treatment"),
                 ("Refer for further tests", "Refer for further tests"),
                 ("Reassure and send home", "Reassure and send home"),
                 ])
    pageblocks = generic.GenericRelation(PageBlock)

    template_file = "exercises/labblock.html"
    display_name = "Exercise"
    exportable = False
    importable = False

    def submit(self, user, data):
        """ a big open question here is whether we should
        be validating submitted answers here, on submission,
        or let them submit whatever garbage they want and only
        worry about it when we show the admins the results """

        # have to group them first
        results = dict()
        abnormalities = dict()
        action_plan = ""
        assessment = ""
        for k in data.keys():
            if k.startswith('result-'):
                tid = int(k[len('result-'):])
                results[tid] = data[k]
            if k.startswith('abnormality-'):
                tid = int(k[len('abnormality-'):])
                abnormalities[tid] = data[k]
            if k == 'action-plan':
                action_plan = data[k]
            if k == 'assessment':
                assessment = data[k]
        ActionPlanResponse.objects.create(
            lab=self, user=user,
            action_plan=action_plan,
            assessment=assessment,
        )
        # now save them
        for tid in results.keys():
            test = Test.objects.get(id=tid)
            result = results[tid]
            abnormality = abnormalities.get(tid, "none")
            TestResponse.objects.create(user=user, test=test,
                                        result_level=result,
                                        abnormality=abnormality)

    def needs_submit(self):
        # labs always require a submit
        return True

    def redirect_to_self_on_submit(self):
        # show the student feedback before proceeding
        return True

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        action_plan_choices = [
            ("Situation urgent. Call or admit patient immediately",
             "Situation urgent. Call or admit patient immediately"),
            ("Situation needs follow-up. Call patient within a week",
             "Situation needs follow-up. Call patient within a week"),
            ("Flag for review at following visit",
             "Flag for review at following visit"),
            ("Call patient's mother to say the results were normal",
             "Call patient's mother to say the results were normal"),
            ("Prescribe treatment", "Prescribe treatment"),
            ("Refer for further tests", "Refer for further tests"),
            ("Reassure and send home", "Reassure and send home"),
        ]

        # once we have the list of answers for sick visits, we'll swap out the
        # choices dynamically here
        class EditForm(forms.Form):
            description = forms.CharField(
                widget=forms.widgets.Textarea(),
                initial=self.description)
            assessment = forms.BooleanField(
                widget=forms.widgets.CheckboxInput,
                initial=self.assessment)
            sickvisit = forms.BooleanField(
                widget=forms.widgets.CheckboxInput,
                initial=self.sickvisit)
            correct_actionplan = forms.ChoiceField(
                widget=forms.widgets.Select,
                initial=self.correct_actionplan,
                choices=action_plan_choices)
            alt_text = ("<a href=\"" + reverse("edit-lab", args=[self.id])
                        + "\">manage tests</a>")
        return EditForm()

    def edit(self, vals, files):
        self.description = vals.get('description', '')
        self.assessment = vals.get('assessment', '')
        self.sickvisit = vals.get('sickvisit', '')
        self.correct_actionplan = vals.get('correct_actionplan', '')
        self.save()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(self, request):
        return Lab.objects.create(
            description=request.POST.get('description', ''))

    def add_test_form(self, request=None):
        class AddTestForm(forms.ModelForm):
            class Meta:
                model = Test
                exclude = ("lab", "ordinality")
        return AddTestForm(request)

    def update_tests_order(self, test_ids):
        for i, qid in enumerate(test_ids):
            test = Test.objects.get(id=qid)
            test.ordinality = i + 1
            test.save()

    def all_abnormalities(self):
        return ["unselected", "No abnormality", "Anemia",
                "Atypical Lymphocytosis", "Bandemia", "Elevated",
                "Eosinopenia", "Eosinophilia", "Erythrocytosis",
                "Erythropenia", "High Atypical Lymphocytosis", "Increased INR",
                "Leukocytosis", "Leukopenia", "Lymphocytosis", "Lymphopenia",
                "Macrocytosis", "Microcytosis", "Moderate Neutropenia",
                "Monocytopenia", "Monocytosis", "Monopenia", "Neutrocytosis",
                "Neutropenia", "Neutropenic", "Neutrophillia", "Polycythemia",
                "Prolonged PT", "Reticulocytosis", "Severe Neutropenia",
                "Thrombocytopenia", "Thrombocytosis"]

    def unlocked(self, user):
        # meaning that the user can proceed *past* this one,
        # not that they can access this one. careful.
        return ActionPlanResponse.objects.filter(
            lab=self, user=user).count() > 0


TEST_CHOICES = (
    ('unselected', 'Please select:'),
    ('low', 'Low'),
    ('normal', 'Normal'),
    ('high', 'High'),
)


class Test(models.Model):
    lab = models.ForeignKey(Lab)
    name = models.CharField(max_length=256)
    ordinality = models.PositiveIntegerField(default=1)
    result = models.CharField(max_length=256)
    normal_range = models.CharField(max_length=256, blank=True)
    unit = models.CharField(max_length=256)
    result_level = models.CharField(max_length=256, choices=TEST_CHOICES,
                                    default="normal")
    abnormality = models.CharField(max_length=256, default="none")

    class Meta:
        ordering = ('lab', 'ordinality')

    def edit_form(self, request=None):
        class F(forms.ModelForm):
            class Meta:
                model = Test
                exclude = ("lab", "ordinality")
        return F(request, instance=self)


class TestResponse(models.Model):
    test = models.ForeignKey(Test)
    user = models.ForeignKey(User)
    result_level = models.CharField(max_length=256, choices=TEST_CHOICES)
    abnormality = models.CharField(max_length=256, default="none")

    def __unicode__(self):
        return "TestResponse (%s, %s)" % (
            unicode(self.test), unicode(self.user))

    def correct_level(self):
        return self.result_level == self.test.result_level

    def correct_abnormality(self):
        return self.abnormality == self.test.abnormality


class ActionPlanResponse(models.Model):
    lab = models.ForeignKey(Lab)
    user = models.ForeignKey(User)
    action_plan = models.CharField(max_length=256, default="")
    assessment = models.TextField(default="", blank=True)

    def __unicode__(self):
        return "ActionPlanResponse for %s" % unicode(self.user)

    def correct_action_plan(self):
        return self.action_plan == self.lab.correct_actionplan
