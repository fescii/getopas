from typing_extensions import Self
from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(Self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated