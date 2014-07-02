from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView
from django.http.response import HttpResponseRedirect
from pagetree.generic.views import PageView, EditView
from pagetree.helpers import get_hierarchy
from pagetree.models import Section, Hierarchy, UserPageVisit
from pedialabsnew.exercises.models import ActionPlanResponse, TestResponse
from quizblock.models import Submission


@render_to('main/index.html')
def index(request):
    ctx = {'survey_complete': False}
    if not request.user.is_anonymous():
        hierarchy = Hierarchy.objects.get(name='labs')
        usersurvey = hierarchy.get_section_from_path('survey')
        if usersurvey.submitted(request.user):
            ctx['survey_complete'] = True
        visits = UserPageVisit.objects.filter(
            user=request.user,
            section__hierarchy=hierarchy).order_by('-last_visit')
        ctx['visits_len'] = len(visits)
        if len(visits) > 0:
            ctx['last_location'] = visits[0].section
        else:
            ctx['last_location'] = hierarchy.get_root()
    return ctx


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class LoggedInMixinStaff(object):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinStaff, self).dispatch(*args, **kwargs)


class LoggedInMixinSuperuser(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinSuperuser, self).dispatch(*args, **kwargs)


class ViewPage(LoggedInMixin, PageView):
    template_name = "pagetree/labs.html"
    hierarchy_name = "labs"
    hierarchy_base = "/pages/labs/"
    gated = True


class EditPage(LoggedInMixinSuperuser, EditView):
    template_name = "pagetree/edit_labs.html"
    hierarchy_name = "labs"
    hierarchy_base = "/pages/labs/"


class ViewPageOverview(PageView):
    template_name = "pagetree/overview.html"
    hierarchy_name = "public"
    hierarchy_base = "/pages/public/"


class EditPageOverview(LoggedInMixinSuperuser, EditView):
    template_name = "pagetree/edit_overview.html"
    hierarchy_name = "public"
    hierarchy_base = "/pages/public/"


class ClearStateView(LoggedInMixinSuperuser, View):
    def get(self, request):
        UserPageVisit.objects.filter(user=request.user).delete()

        # clear quiz
        submissions = Submission.objects.filter(user=request.user)
        submissions.delete()

        # clear exercises
        responses = ActionPlanResponse.objects.filter(user=request.user)
        responses.delete()
        responses = TestResponse.objects.filter(user=request.user)
        responses.delete()

        return HttpResponseRedirect("/")


class InstructorPage(LoggedInMixinStaff, TemplateView):
    template_name = "main/instructor_index.html"

    def get_context_data(self, **kwargs):
        context = super(InstructorPage, self).get_context_data(**kwargs)
        h = get_hierarchy('labs')
        root = h.get_root()
        all_modules = root.get_children()
        context['students'] = User.objects.all()
        context['all_modules'] = all_modules

        return context


class InstructorLabReport(LoggedInMixinStaff, TemplateView):
    template_name = "main/instructor_lab_report.html"

    def has_lab(self, section):
        for p in section.pageblock_set.all():
            if p.block().display_name == "Lab Exercise":
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(InstructorLabReport, self).get_context_data(**kwargs)
        uni = self.kwargs['uni']
        module_id = self.kwargs['module_id']
        student = User.objects.get(username=uni)
        module = Section.objects.get(id=module_id)
        labs = [s for s in module.get_descendants() if self.has_lab(s)]
        lab_section = None
        lab_block = None
        if 'lab' in self.request.GET:
            lab_section = Section.objects.get(id=self.request.GET['lab'])
            lab_block = [p.block() for p in lab_section.pageblock_set.all()
                         if p.block().display_name == "Lab Exercise"][0]
        r = ActionPlanResponse.objects.filter(lab=lab_block, user=student)

        context['student'] = student
        context['module'] = module
        context['labs'] = labs
        context['lab_block'] = lab_block
        context['lab_section'] = lab_section
        context['taken'] = r.count() > 0

        return context
