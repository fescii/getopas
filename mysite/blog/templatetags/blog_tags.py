from actions.models import Action,UserAction
from magazine.models import Issue_likes
import readtime
from django.shortcuts import render,get_object_or_404
from django import template
from ..models import Post,Bookmark,Like,BlogComment
from django.db.models import Count
from django.template.defaultfilters import slugify
from unidecode import unidecode
from taggit.models import Tag
from django.contrib.auth.models import User
from account.models import Contact
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

#Get Total Published Posts
@register.simple_tag
def total_posts():
    return Post.published.count()

#Get Total Unread Notification
@register.simple_tag
def total_unread(user_id):
    a_user = User.objects.get(id=user_id)
    actions = Action.objects.exclude(user=a_user)
    following_ids = a_user.following.values_list('id',flat=True)
    user_action_ids = UserAction.objects.filter(user=a_user,deleted=True)
    user_action_ids = user_action_ids.values_list('action',flat=True)
    user_read_ids = UserAction.objects.filter(user=a_user,status='read').values_list('action',flat=True)
    total = 0
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
                .prefetch_related('target')
    actions = actions.exclude(id__in=user_action_ids)
    total = actions.exclude(id__in=user_read_ids).count()
    return total



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


#Check-if-post-is-saved
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

#Check-if-comment-is-liked
@register.simple_tag
def check_comment(comment,user):
    target_comment = BlogComment.objects.get(id=comment)
    if target_comment.author.id == user:
        return 'Delete'
    else:
        try:
            liked_comment = Like.objects.get(comment=comment,user=user)
            if liked_comment:
                return 'Unlike'
            else:
                return 'Like'
        except Like.DoesNotExist:
            return 'Like'

#Check-if-post-is-saved
@register.simple_tag
def check_liked(id,user):
    try:
        saved_issue = Issue_likes.objects.get(issue=id,user=user)
        if saved_issue:
            return 'unlike'
        else:
            return 'like'
    except Issue_likes.DoesNotExist:
        return 'like'
#register.filter('check_saved',check_saved)

#Check-if-user-is-followed
@register.simple_tag
def check_user_follow(user_id,user):
    a_user = User.objects.get(id=user_id)
    if Contact.objects.filter(user_from=user,user_to=a_user):
        return 'unfollow'
    else:
        return 'follow'

#Check-if-notification-is-read
@register.simple_tag
def check_read(id,user):
    user = User.objects.get(id=user)
    action = Action.objects.get(id=id)
    try:
        user_action = UserAction.objects.get(action=action,user=user)
        if user_action.status == 'unread':
            return 'read'
        else:
            return 'unread'
    except UserAction.DoesNotExist:
        return 'read'

#Check-if-notification-is-removed
@register.simple_tag
def check_removed(id,user):
    user = User.objects.get(id=user)
    action = Action.objects.get(id=id)
    try:
        user_action = UserAction.objects.get(action=action,user=user)
        if user_action.deleted == True:
            return 'redo'
        else:
            return 'delete'
    except UserAction.DoesNotExist:
        return 'delete'

#Truncate Tags
def truncate_tags(tags):
    return tags[:3]

register.filter('truncate_tags',truncate_tags)

#Return-First Tag
def first_tag(tags):
    return tags[:1]

register.filter('first_tag',first_tag)

#Slugify Tags
def slug_tag(tag):
   return slugify(unidecode(tag))

register.filter('slug_tag',slug_tag)

#Total Posts For Tags
def post_no(topic=None):
    if topic:
        tag = get_object_or_404(Tag, slug=topic)
        posts = Post.published.filter(tags__in=[tag]).count()
    return posts

register.filter('post_no',post_no)

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

#Getting Total comments an-article
def get_article_comments(post_id):
    article = Post.published.get(id=post_id)
    try:
        comments = article.comments.filter(active=True).count()
    except:
        comments = 0
    return comments
register.filter('get_article_comments',get_article_comments)

def split(string, sep):
    #Return the string split by sep.
    try:
        splitted = str(string).split(sep)
        word = " "
        for text in splitted:
             word = word+" "+text.capitalize()
        #word = f"{splitted[0].capitalize()} {splitted[1].capitalize()}"
        return word
    except:
        return str(string).capitalize()
register.filter('split',split)

#Return tine-since-the-article-was-posted
def time_lapse(posted_time):
    time_now = datetime.now()
    posted_time = posted_time
    delta = time_now - posted_time
    seconds = delta.total_seconds()
    if(seconds < 60):
        return f'{round(seconds)} seconds ago'
    elif(seconds > 60 and seconds < 3600):
        mins = round(seconds/60)
        if(mins>1):
            return f'{mins} minutes ago'
        else:
            return f'{mins} minute ago'
    elif(seconds > 3600 and seconds < 86400):
        hours = round(seconds/3600)
        if(hours>1):
            return f'{hours} hours ago'
        else:
            return f'{hours} hour ago'
    elif(seconds > 86400 and seconds < 604800):
        day = posted_time.strftime('%A')
        day_time = posted_time.strftime('%H:%M')
        return f'{day} at {day_time}'
    elif(seconds > 604800 and seconds < 2628002):
        days = delta.days
        return f'{days} days ago'
    elif(seconds > 2628002 and seconds < 31536000):
        months = round(seconds/2628002)
        if(months>1):
            return f'{months} months ago'
        else:
            return f'{months} month ago'
    elif(seconds > 31536000):
        years = round(seconds/31536000)
        if(years>1):
            return f'{years} years ago'
        else:
            return f'{years} year ago'
register.filter('time_lapse',time_lapse)

#Return tine-since-the-article-was-posted
def get_date_en(posted_time):
    posted_time = posted_time
    th = ''
    day = int(posted_time.strftime('%d'))
    if (day == 11):
        th = 'th'
    elif (day == 12):
        th = 'th'
    elif (day == 13):
        th = 'th'
    else:
        if ((day % 10) == 1):
            th = 'st'
        elif ((day % 10) == 2):
            th = 'nd'
        elif ((day % 10) == 3):
            th = 'rd'
        else:
            th = 'th'
    return f"{day}{th} {posted_time.strftime('%b')} {posted_time.strftime('%Y')}"
register.filter('get_date_en',get_date_en)