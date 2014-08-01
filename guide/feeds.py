from django.contrib.syndication.feeds import Feed
from pdxguide.guide.models import Article
import datetime

class ArticleFeed(Feed):
    title = "Zinester's Guide to Portland Articles"
    link = "http://pdxguide.org/browse/"
    description = "The latest articles from pdxguide.org."

    def items(self):
        return Article.objects.filter(date_modified__lte=datetime.datetime.now()).filter(status__in=['A','B']).order_by('-date_added')[:10]

