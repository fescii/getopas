from django.contrib.sitemaps import Sitemap
from .models import Issue

class IssueSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(Self):
        return Issue.published.all()

    def lastmod(self, obj):
        return obj.updated