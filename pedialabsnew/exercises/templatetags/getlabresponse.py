from django import template
from ..models import TestResponse, ActionPlanResponse

register = template.Library()


class GetTestResponseNode(template.Node):
    def __init__(self, test, var_name):
        self.test = test
        self.var_name = var_name

    def render(self, context):
        t = context[self.test]
        u = context['request'].user
        r = TestResponse.objects.filter(test=t, user=u)
        if r.count() > 0:
            context[self.var_name] = r[0]
        else:
            context[self.var_name] = None
        return ''


@register.tag('gettestresponse')
def gettestresponse(parser, token):
    test = token.split_contents()[1:][0]
    var_name = token.split_contents()[1:][2]
    return GetTestResponseNode(test, var_name)


class GetActionPlanResponseNode(template.Node):
    def __init__(self, lab, var_name):
        self.lab = lab
        self.var_name = var_name

    def render(self, context):
        l = context[self.lab]
        u = context['request'].user
        r = ActionPlanResponse.objects.filter(lab=l, user=u)
        context[self.var_name] = r[0]
        return ''


@register.tag('getactionplanresponse')
def getactionplanresponse(parser, token):
    lab = token.split_contents()[1:][0]
    var_name = token.split_contents()[1:][2]
    return GetActionPlanResponseNode(lab, var_name)


class GetStudentTestResponseNode(template.Node):
    def __init__(self, test, student, var_name):
        self.test = test
        self.student = student
        self.var_name = var_name

    def render(self, context):
        t = context[self.test]
        u = context[self.student]
        r = TestResponse.objects.filter(test=t, user=u)
        context[self.var_name] = r[0]
        return ''


@register.tag('getstudenttestresponse')
def getstudenttestresponse(parser, token):
    test = token.split_contents()[1:][0]
    student = token.split_contents()[1:][1]
    var_name = token.split_contents()[1:][3]
    return GetStudentTestResponseNode(test, student, var_name)


class GetStudentActionPlanResponseNode(template.Node):
    def __init__(self, lab, student, var_name):
        self.lab = lab
        self.student = student
        self.var_name = var_name

    def render(self, context):
        l = context[self.lab]
        u = context[self.student]
        r = ActionPlanResponse.objects.filter(lab=l, user=u)
        context[self.var_name] = r[0]
        return ''


@register.tag('getstudentactionplanresponse')
def getstudentactionplanresponse(parser, token):
    lab = token.split_contents()[1:][0]
    student = token.split_contents()[1:][1]
    var_name = token.split_contents()[1:][3]
    return GetStudentActionPlanResponseNode(lab, student, var_name)
