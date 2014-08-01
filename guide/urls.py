from django.conf.urls.defaults import *
from pdxguide.guide.models import *
import datetime

article_dict = {
    # 'queryset': Article.objects.filter(date_modified__lte=datetime.datetime.now()).filter(status__in=['A','B']).order_by('-date_modified'),
    'queryset': Article.objects.all(),
    'template_object_name': 'article',
}
quadrant_dict = {
    'queryset': Quadrant.objects.all(),
    'template_object_name': 'quadrant',
}
all_section_dict = {
    'queryset': Section.objects.all(),
    'template_object_name': 'section',
}
section_dict = {
    'queryset': Section.objects.all(),
    'template_object_name': 'section',
}

        
urlpatterns = patterns('',
    # /browse/all
    (r'^all/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(all_section_dict, slug_field='slug', template_name="guide/section_detail.html")),
    # /browse/northwest/
    (r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(quadrant_dict, slug_field='slug')),
    # /browse/northwest/bars/ -- todo: filter by quadrant
    (r'^(?P<quadrant_slug>[-\w]+)/(?P<section_slug>[-\w]+)/$', 'pdxguide.guide.views.section_by_quadrant'),
    # /browse/northwest/bars/angelos/
    (r'^([-\w]+)/([-\w]+)/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(article_dict, slug_field='slug')),

)

# pdxguide.org/browse/<quadrant>/<section>/<slug> -- shows single entry
# pdxguide.org/browse/<quadrant>/<section> -- shows all section in quadrant
# pdxguide.org/browse/<quadrant> -- shows all in quadrant
# pdxguide.org/browse/all/<section> -- shows all of ie: "record stores"

# pdxguide.org/browse/southeast/grocery/fred-meyers
# pdxguide.org/browse/northeast/record-stores/mississippi-records
# pdxguide.org/browse/
# pdxguide.org/browse/highest-rated/
# pdxguide.org/browse/latest/
# pdxguide.org/browse/ -- shows most recent entries

# FLATPAGES
# pdxguide.org/contact/ 
# pdxguide.org/printcopy/
# pdxguide.org/faq/
