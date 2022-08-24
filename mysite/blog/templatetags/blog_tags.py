from django import template
from ..models import Post

register = template.Library

@register.simple_tag(name="total_posts")
def total_posts():
    return Post.published.count()