from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from pagetree.generic.views import PageView, EditView, InstructorView
from pagetree.helpers import get_hierarchy
from pagetree.models import Section
from pedialabsnew.exercises.models import ActionPlanResponse


@render_to('main/index.html')
def index(request):
    # import pdb
    # pdb.set_trace()
    return dict()


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


class InstructorPage(LoggedInMixinStaff, InstructorView):
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


@render_to('main/instructor_index.html')
def instructor_index(request):
    h = get_hierarchy()
    root = h.get_root()
    all_modules = root.get_children()
    return dict(students=User.objects.all(),
                all_modules=all_modules)


def has_lab(section):
    for p in section.pageblock_set.all():
        if p.block().display_name == "Lab":
            return True
    return False


@render_to('main/instructor_lab_report.html')
def instructor_lab_report(request, uni, module_id):
    student = User.objects.get(username=uni)
    module = Section.objects.get(id=module_id)
    labs = [s for s in module.get_descendents() if has_lab(s)]
    lab_section = None
    lab_block = None
    if 'lab' in request.GET:
        lab_section = Section.objects.get(id=request.GET['lab'])
        lab_block = [p.block() for p in lab_section.pageblock_set.all()
                     if p.block().display_name == "Lab"][0]
    r = ActionPlanResponse.objects.filter(lab=lab_block, user=student)
    return dict(student=student, module=module, labs=labs,
                lab_block=lab_block, lab_section=lab_section,
                taken=r.count() > 0)
