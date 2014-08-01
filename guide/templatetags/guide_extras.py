from django import template
from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from pdxguide.guide.models import Article
import datetime
     
register = Library()
     
class LatestContentNode(Node):
    """
    {% get_latest weblog.Entry 10 as latest_entries %}
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "fourth argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

class LatestArticles(Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        context[self.varname] = Article.objects.filter(status__in=['A','B']).order_by('-date_added')[:self.num]
        return ''

def get_latest_articles(parser, token):
    """
    {% get_latest_articles 6 as article_list %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    return LatestArticles(bits[1], bits[3])

class MapBounds(Node):
    def __init__(self, quadrant_id, varname):
        self.quadrant_id, self.varname = quadrant_id, varname

    def render(self, context):
        from django.db import connection
        sql = "SELECT avg(latitude) AS lat_avg, avg(longitude) AS lon_avg,"
        sql += "max(latitude) AS lat_max,min(latitude) AS lat_min,"
        sql += "max(longitude) AS lon_max, min(longitude) AS lon_min FROM guide_article WHERE "
        sql +=  "quadrant_id = '%s'" % (self.quadrant_id)
        sql += " AND latitude != 0 AND longitude != 0"
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone();
        context[self.varname] = row
        return ''

def get_map_bounds(parser, token):
    """
    {% get_map_bounds 6 as map_bounds %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    return MapBounds(bits[1], bits[3])

get_latest = register.tag(get_latest)
get_latest_articles = register.tag(get_latest_articles)
get_map_bounds = register.tag(get_map_bounds)

def paginator(context, adjacent_pages=2):
    """Adds pagination context variables for first, adjacent and next page links
    in addition to those already populated by the object_list generic view."""
    page_numbers = [n for n in \
                    range(context["page"] - adjacent_pages, context["page"] + adjacent_pages + 1) \
                    if n > 0 and n <= context["pages"]]
    return {
        "hits": context["hits"],
        "results_per_page": context["results_per_page"],
        "page": context["page"],
        "pages": context["pages"],
        "page_numbers": page_numbers,
        "next": context["next"],
        "previous": context["previous"],
        "has_next": context["has_next"],
        "has_previous": context["has_previous"],
        "show_first": 1 not in page_numbers,
        "show_last": context["pages"] not in page_numbers,
        "q": context["q"],
    }

register.inclusion_tag("paginator.html", takes_context=True)(paginator)