from django import template

register = template.Library()


class AccessibleNode(template.Node):
    def __init__(self, section, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.section = section

    def render(self, context):
        s = context[self.section]
        r = context['request']
        u = r.user
        if section.gate_check(u[0]) and section.submitted(u):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('ifaccessible')
def accessible(parser, token):
    section = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else', 'endifaccessible'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifaccessible',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return AccessibleNode(section, nodelist_true, nodelist_false)


class SubmittedNode(template.Node):
    def __init__(self, block, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.block = block

    def render(self, context):
        s = context[self.block]
        r = context['request']
        u = r.user
        if block_submitted(s, u):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('ifsubmitted')
def submitted(parser, token):
    block = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else', 'endifsubmitted'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifsubmitted',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return SubmittedNode(block, nodelist_true, nodelist_false)
