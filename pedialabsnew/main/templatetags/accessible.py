from django import template

register = template.Library()


def block_submitted(block, user):
    if user.is_anonymous():
        # anon can't have submitted a block
        return False
    if hasattr(block, 'needs_submit'):
        if block.needs_submit():
            try:
                s = block.unlocked(user)
                if not s:
                    return False
            except:
                pass
    return True


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
