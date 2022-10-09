import readtime
from django import template
from ..models import Post,Bookmark
from django.db.models import Count
from django.template.defaultfilters import slugify
from unidecode import unidecode

register = template.Library()

#Get Total Published Posts
@register.simple_tag
def total_posts():
    return Post.published.count()

#Get five latest posts
@register.simple_tag
def show_latest_posts(count=5):
    return Post.published.order_by('-publish')[:count]

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
#Truncate Tags
def truncate_tags(tags):
    return tags[:3]

register.filter('truncate_tags',truncate_tags)

#Slugify Tags
def slug_tag(tag):
   return slugify(unidecode(tag))

register.filter('slug_tag',slug_tag)

#Fetching 4 most viewed  Blog
@register.inclusion_tag('blog/post/tags.html')
def show_most_common_tags(count=15):
    common_tags = Post.tags.most_common()[:count]
    return {'common_tags': common_tags}

#Getting Total articles views of the current user
def get_views(user):
    user_articles = Post.published.filter(author=user)
    count = 0
    for article in user_articles:
        count = count + article.blog_views
    return count
register.filter('get_views',get_views)

#Getting Total articles comments of the current user
def get_comments(user):
    user_articles = Post.published.filter(author=user)
    comments = 0
    for article in user_articles:
        if article.comments:
            com = article.comments.filter(active=True).count()
            comments = comments + com
    return comments
register.filter('get_comments',get_comments)


def split(string, sep):
    #Return the string split by sep.
    try:
        splitted = string.split(sep)
        word = " "
        for text in splitted:
             word = word+ " "+text.capitalize()
        #word = f"{splitted[0].capitalize()} {splitted[1].capitalize()}"
        return word
    except:
        return string.capitalize()
register.filter('split',split)