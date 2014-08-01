from django.conf.urls.defaults import *
from pdxguide.tags.models import Tag
from pdxguide.guide.feeds import *
from django.contrib.comments.feeds import LatestFreeCommentsFeed
from django.contrib.comments.models import FreeComment

tag_dict = {
    'queryset': Tag.objects.all(), 
}

comments_info_dict = {
    'queryset': FreeComment.objects.all(),
    'paginate_by': 15,
}

feeds = {
    'articles': ArticleFeed,
    'comments': LatestFreeCommentsFeed,
}


# feeds = {
#     'latest': LatestEntries,
#     'categories': LatestEntriesByCategory,
# }

urlpatterns = patterns('',
     (r'^clearcache$', 'pdxguide.guide.views.clearcache'),
     # (r'^move_essays/(?P<quadrant_id>[\d]+)/(?P<start>[\d]+)/(?P<stop>[\d]+)/$', 'pdxguide.guide.utils.move_essays'),  
     # (r'^fix_phone_numbers/(?P<start>[\d]+)/(?P<stop>[\d]+)/$', 'pdxguide.guide.utils.fix_phone_numbers'),  
     # (r'^fix_slugs/(?P<start>[\d]+)/(?P<stop>[\d]+)/$', 'pdxguide.guide.utils.fix_slugs'),  
     (r'^new_articles/(?P<date_start>[\d\-]+)/$', 'pdxguide.guide.utils.new_articles'),  
     # (r'^get_geocodes/(?P<start>[\d]+)/(?P<stop>[\d]+)/$', 'pdxguide.guide.utils.get_geocodes'),  
     (r'^search/$', 'pdxguide.guide.views.search'),  
     (r'^contact/$', 'pdxguide.guide.views.contact_form'),  
     (r'^submit/$', 'pdxguide.guide.views.submit_article'),  
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
     (r'^comments/', include('django.contrib.comments.urls.comments')),
     (r'^tag/(?P<id>[A-Za-z-_]+)/$','django.views.generic.list_detail.object_detail', dict(tag_dict)),
     (r'^browse/', include('pdxguide.guide.urls')),
     (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
     (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/home/natebeaty/django/django_projects/pdxguide/admin_media/'}),
     (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'django.conf'}),
     # (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/home/natebeaty/django/django_projects/pdxguide/media/'}),
     (r'', include('django.contrib.flatpages.urls')),
)
