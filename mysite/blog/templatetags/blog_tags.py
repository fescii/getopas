import readtime
from django import template
from ..models import Post,Bookmark
from django.db.models import Count

register = template.Library()

#Get Total Published Posts
@register.simple_tag
def total_posts():
    return Post.published.count()

#Get five latest posts
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

#Get Most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments = Count('comments')).order_by('-total_comments')[:count]


#Fetching 4 most viewed  Blog
@register.inclusion_tag('blog/post/most_viewed.html')
def show_most_viewed_posts(count=4):
    most_viewed = Post.published.order_by('-blog_views')[:count]
    return {'most_viewed': most_viewed}

def read_time(html):
    return readtime.of_html(html)

register.filter('read_time',read_time)


#Get Most commented posts
@register.simple_tag
def check_saved(id,user):
    try:
        saved_post = Bookmark.objects.get(post=id,user=user)
        if saved_post:
            return 'Remove'
        else:
            return 'Save'
    except Bookmark.DoesNotExist:
        return 'Save'
#register.filter('check_saved',check_saved)