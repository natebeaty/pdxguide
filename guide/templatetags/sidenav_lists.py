from django import template
from pdxguide.guide.models import Quadrant, Section
import datetime

class QuadrantList(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = list(Quadrant.objects.filter(status__in=['W','A']))
        return ''

class SectionList(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = list(Section.objects.filter(status__in=['W','A']))
        return ''

def do_get_quadrant_list(parser, token):
    """
    {% get_quadrant_list as quadrant_list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    return QuadrantList(bits[2])

def do_get_section_list(parser, token):
    """
    {% get_section_list as section_list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    return SectionList(bits[2])

register = template.Library()
register.tag('get_quadrant_list', do_get_quadrant_list)
register.tag('get_section_list', do_get_section_list)
