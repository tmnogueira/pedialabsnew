from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from pagetree.helpers import get_hierarchy
from pagetree.generic.views import PageView, EditView, InstructorView


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
    hierarchy_name = "labs"
    hierarchy_base = "/pages/labs/"


class EditPage(LoggedInMixinSuperuser, EditView):
    hierarchy_name = "labs"
    hierarchy_base = "/pages/labs/"


class InstructorPage(LoggedInMixinStaff, InstructorView):
    hierarchy_name = "labs"
    hierarchy_base = "/pages/labs/"


class EditPageOverview(LoggedInMixinSuperuser, EditView):
    hierarchy_name = "public"
    hierarchy_base = "/pages/public/"


