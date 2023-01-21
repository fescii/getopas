from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login
import json

from magazine.models import Issue, Issue_likes
from .forms import  CreateBlogPostForm,\
        BlogEditForm, CreateMagazineForm, MagazineEditForm,\
             MagazineEditTagsForm,\
                BlogEditTagsForm, BlogEditCoverForm,\
                    MagazineEditCoverForm
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from account.views import is_admin, is_editor, is_author
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from account.models import Profile,Theme,UserTheme
from blog.models import Post,Bookmark,Like,BlogComment
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from taggit.models import Tag
from actions.utils import create_action,create_user_action
from actions.models import Action,UserAction
from account.models import Contact
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
#Home
def main_home(request):
    # Display all posts by default
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    post_only = request.GET.get('story_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        return render(request,
                      'main/list-stories.html',
                      {'section': 'stories','stories': posts})

    return render(request,
                 'main/main.html',
                    {'stories':posts,
                    'title':'home',
                    'section':'opas'})



#Dashboard
@login_required
def dashboard(request):
    user = request.user
    profile = user.profile

    # Display all actions by default
    posts_interest = Post.published.exclude(author=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        posts_interest = posts_interest.filter(author__in=following_ids)
        posts_interest = posts_interest.select_related('author', 'author__profile')[:5]
    #Top Posts
    top_posts = Post.most_viewed(Post)

    #Recent Added-Posts
    recently_added = Post.recently_added(Post, 5)

    return render(request,
                 'editors/dashboard.html',
                    {'user': user,
                    'profile': profile,
                    'most_viewed':top_posts,
                    'posts_interest':posts_interest,
                    'recently_added': recently_added,
                    'title':'home','tab': 'opas',
                    'section':'opas'})

#Dashboard-Newsletters
@login_required
def newsletters(request):
    user = request.user
    profile = user.profile

    # Display issues-with-most-common-tags
    common_tags = Issue.tags.most_common()[:5]
    issues_interest = Issue.published.filter(tags__in=common_tags).distinct()[:6]
    #Top Posts
    top_issues = Issue.most_liked(Issue,6)

    #Recent Added-Posts
    recently_added = Issue.recently_added(Issue, 6)

    return render(request,
                 'editors/newsletters.html',
                    {'user': user,
                    'profile': profile,
                    'most_liked':top_issues,
                    'issues_interest':issues_interest,
                    'recently_added': recently_added,
                    'title':'newsletters','tab': 'newsletters',
                    'section':'newsletters'})

# Like Newsletters
@login_required
@require_POST
def like_newsletter(request):
    issue_id = request.POST.get('id')
    action = request.POST.get('action')
    if issue_id and action:
        try:
            issue = Issue.objects.get(id=issue_id)
            try:
                liked_issue = Issue_likes.objects.get(issue=issue,user=request.user)
                liked_issue.delete()
                return JsonResponse({'status': 'ok','action': 'like'})
            except Issue_likes.DoesNotExist:
                issue_like = Issue_likes.objects.create(issue=issue,user=request.user)
                issue_like.save()
                #create_action(request.user, 'likes newsletter','like', issue)
                return JsonResponse({'status': 'ok','action': 'unlike'})
        except Issue.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

#Explore
@login_required
def explore_newsletter_topic(request,topic=None):
    user = request.user
    profile = user.profile

    #Getting Total articles views and comments of the current user
    object_list = Issue.published.all()
    tag = None
    if topic:
        tag = get_object_or_404(Tag, slug=topic)
        topic_issues = object_list.filter(tags__in=[tag])
    paginator = Paginator(topic_issues, 15) # 5 posts in each page
    page = request.GET.get('page')
    try:
        topic_issues = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        topic_issues = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        topic_issues = paginator.page(paginator.num_pages)

    return render(request,
                 'editors/explore-newsletter.html',
                    {'user': user,
                    'profile': profile,
                    'topic': topic,
                    'section':'newsletters',
                    'title': 'explore','tab': 'newsletters',
                    'topic_issues': topic_issues})

#Feeds Infinite Scroll.
@login_required
def popular_newsletters(request):
    issues = Issue.published.annotate(total_comments = Count('issue_likes')).order_by('-total_comments')
    paginator = Paginator(issues, 6)
    page = request.GET.get('page')
    issue_only = request.GET.get('issue_only')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
        if issue_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        issues = paginator.page(paginator.num_pages)
    if issue_only:
        return render(request,
        'editors/list-newsletters.html',
        {'section': 'newsletters',
         'issues': issues})

    return render(request,
                  'editors/newsletter-feed.html',
                  {'title': 'popular','tab': 'newsletters',
                   'section': 'newsletters',
                   'issues': issues})
#Feeds Infinite Scroll.
@login_required
def interest_newsletters(request):
    # Display issues-with-most-common-tags
    common_tags = Issue.tags.most_common()[:15]
    issues = Issue.published.filter(tags__in=common_tags).distinct()
    paginator = Paginator(issues, 6)
    page = request.GET.get('page')
    issue_only = request.GET.get('issue_only')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
        if issue_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        issues = paginator.page(paginator.num_pages)
    if issue_only:
        return render(request,
        'editors/list-newsletters.html',
        {'section': 'newsletters',
         'issues': issues})

    return render(request,
                  'editors/newsletter-feed.html',
                  {'title': 'for you','tab': 'newsletters',
                   'section': 'newsletters',
                   'issues': issues})
#Feeds Infinite Scroll.
@login_required
def recent_newsletters(request):
    # Display recent-recent-newsletters
    issues = Issue.published.order_by('-publish')
    paginator = Paginator(issues, 6)
    page = request.GET.get('page')
    issue_only = request.GET.get('issue_only')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
        if issue_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        issues = paginator.page(paginator.num_pages)
    if issue_only:
        return render(request,
        'editors/list-newsletters.html',
        {'section': 'newsletters',
         'issues': issues})

    return render(request,
                  'editors/newsletter-feed.html',
                  {'title': 'recent','tab': 'newsletters',
                   'section': 'newsletters',
                   'issues': issues})


#Explore
# @login_required
def explore(request,topic=None):
    #Getting Total articles views and comments of the current user
    object_list = Post.published.all()
    tag = None
    if topic:
        tag = get_object_or_404(Tag, slug=topic)
        topic_posts = object_list.filter(tags__in=[tag])

    posts = topic_posts
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    post_only = request.GET.get('story_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        if request.user.is_authenticated:
            return render(request,
                      'main/list-login.html',
                      {'stories': posts})
        else:
            return render(request,
                          'main/list-stories.html',
                            {'stories': posts})

    return render(request,
                 'editors/explore.html',
                    {'topic': topic,
                    'section': 'explore',
                    'title': 'explore','tab': 'opas',
                    'stories': posts})

#Feeds Infinite Scroll.
@login_required
def feeds(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    post_only = request.GET.get('post_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        return render(request,
        'editors/list-feeds.html',
        {'section': 'articles',
         'posts': posts})

    return render(request,
                  'editors/feed.html',
                  {'title': 'feeds','tab': 'opas',
                   'section': 'articles',
                   'posts': posts})

#Feeds Infinite Scroll.
@login_required
def explore_topics(request):
    #Getting Total articles
    object_list = Post.published.all()

    # Most common tags
    most_common_tags = Post.tags.most_common()[:4]
    common_tags = [int(tag.id) for tag in most_common_tags]

    #Posts-in-most-common-tags
    posts_in_tag_one = object_list.filter(tags__in=common_tags[0:1])[:5]
    posts_in_tag_two = object_list.filter(tags__in=common_tags[1:2])[:5]
    posts_in_tag_three = object_list.filter(tags__in=common_tags[2:3])[:5]
    posts_in_tag_four = object_list.filter(tags__in=common_tags[3:4])[:5]


    return render(request,
                  'editors/explore-topics.html',
                  {'title': 'topics','tab': 'opas',
                   'section': 'explore',
                   'tag_one_posts': posts_in_tag_one,
                   'tag_two_posts': posts_in_tag_two,
                   'tag_three_posts': posts_in_tag_three,
                   'tag_four_posts': posts_in_tag_four,
                   'common_tags': most_common_tags})


#Feeds Interests.
@login_required
def interest(request):
     # Display all actions by default
    posts_interest = Post.objects.exclude(author=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        posts_interest = posts_interest.filter(author__in=following_ids)
        posts_interest = posts_interest.select_related('author', 'author__profile')
    paginator = Paginator(posts_interest, 5)
    page = request.GET.get('page')
    post_only = request.GET.get('post_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        return render(request,
        'editors/list-feeds.html',
        {'section': 'articles',
         'posts': posts})

    return render(request,
                  'editors/feed.html',
                  {'title': 'for you','tab': 'opas',
                   'section': 'articles',
                   'posts': posts})

#Feeds Infinite Scroll.
@login_required
def trending(request):
    posts = Post.published.all().order_by('-blog_views')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    post_only = request.GET.get('post_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        return render(request,
        'editors/list-feeds.html',
        {'section': 'articles',
         'posts': posts})

    return render(request,
                  'editors/feed.html',
                  {'title': 'trending','tab': 'opas',
                   'section': 'articles',
                   'posts': posts})

#Feeds Infinite Scroll.
@login_required
def recent(request):
    posts = Post.published.all().order_by('-publish')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    post_only = request.GET.get('post_only')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if post_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        posts = paginator.page(paginator.num_pages)
    if post_only:
        return render(request,
        'editors/list-feeds.html',
        {'section': 'articles',
         'posts': posts})

    return render(request,
                  'editors/feed.html',
                  {'title': 'recent','tab': 'opas',
                   'section': 'articles',
                   'posts': posts})

#Actions.
@login_required
def actions(request):
    # Display all actions by default
    action_only = request.GET.get('action_only')
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')
    user_action_ids = UserAction.objects.filter(user=request.user,deleted=True)
    user_action_ids = user_action_ids.values_list('action',flat=True)
    if user_action_ids:
        actions = actions.exclude(id__in=user_action_ids)

    paginator = Paginator(actions, 10)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if action_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        actions = paginator.page(paginator.num_pages)
    if action_only:
        return render(request,'editors/list-actions.html',
                      {'section': 'notifications','actions': actions})
    return render(request,
                  'editors/actions.html',
                  {'section': 'notifications',
                   'title': 'notifications',
                   'actions': actions})

#Actions.
@login_required
def read_actions(request):
    # Display all actions by default
    action_only = request.GET.get('action_only')
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')
    user_action_ids = UserAction.objects.filter(user=request.user,deleted=True)
    user_action_ids = user_action_ids.values_list('action',flat=True)
    user_unread_ids = UserAction.objects.filter(user=request.user,status='read').values_list('action',flat=True)
    if user_action_ids:
        actions = actions.exclude(id__in=user_action_ids)

    actions = actions.filter(id__in=user_unread_ids)

    paginator = Paginator(actions, 10)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if action_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        actions = paginator.page(paginator.num_pages)
    if action_only:
        return render(request,'editors/list-actions.html',
                      {'section': 'notifications','actions': actions})
    return render(request,
                  'editors/actions.html',
                  {'section': 'notifications',
                   'title': 'read',
                   'actions': actions})

#Actions.
@login_required
def removed_actions(request):
    # Display all actions by default
    action_only = request.GET.get('action_only')
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')
    user_action_ids = UserAction.objects.filter(user=request.user,deleted=True).values_list('action',flat=True)
    actions = actions.filter(id__in=user_action_ids)

    paginator = Paginator(actions, 10)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if action_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        actions = paginator.page(paginator.num_pages)
    if action_only:
        return render(request,'editors/list-actions.html',
                      {'section': 'notifications','actions': actions})
    return render(request,
                  'editors/actions.html',
                  {'section': 'notifications',
                   'title': 'removed',
                   'actions': actions})

#Actions.
@login_required
def unread_actions(request):
    # Display all actions by default
    action_only = request.GET.get('action_only')
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    user_action_ids = UserAction.objects.filter(user=request.user,deleted=True)
    user_action_ids = user_action_ids.values_list('action',flat=True)
    user_read_ids = UserAction.objects.filter(user=request.user,status='read').values_list('action',flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
                .prefetch_related('target')
    actions = actions.exclude(id__in=user_action_ids)
    actions = actions.exclude(id__in=user_read_ids)

    paginator = Paginator(actions, 10)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if action_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        actions = paginator.page(paginator.num_pages)
    if action_only:
        return render(request,'editors/list-actions.html',
                      {'section': 'notifications','actions': actions})
    return render(request,
                  'editors/actions.html',
                  {'section': 'notifications',
                   'title': 'unread',
                   'actions': actions})

#Saved-Posts
@login_required
def my_list(request):
    user = request.user

    #Getting Saved-Posts
    saved_posts = Bookmark.objects.filter(user=user).order_by('-added')

    paginator = Paginator(saved_posts, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                 'editors/bookmark.html',
                    {'saved_posts': posts,
                    'title': 'bookmarks',
                    'section': 'my-list'})

# Add-Post-To-My-list
@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            try:
                saved_post = Bookmark.objects.get(post=post,user=request.user)
                saved_post.delete()
                #create_action(request.user, 'remove from saved','remove', post)
                return JsonResponse({'status': 'ok','action': 'Save'})
            except Bookmark.DoesNotExist:
                bookmark = Bookmark.objects.create(post=post,user=request.user)
                bookmark.save()
                create_action(request.user, 'bookmarked','save', post)
                return JsonResponse({'status': 'ok','action': 'Remove'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

# Add-Post-To-My-list
@login_required
@require_POST
def like_comment(request):
    comment_id = request.POST.get('id')
    #post_id = request.POST.get('post')
    action = request.POST.get('action')
    #post = Post.objects.get(id=post_id)
    if comment_id and action:
        if str(action) == 'Delete':
            comment = BlogComment.objects.get(id=comment_id)
            BlogComment.update_active(comment,False)
            return JsonResponse({'status': 'ok','action': 'Deleted'})
        else:
            comment = BlogComment.objects.get(id=comment_id)
            try:
                liked_comment = Like.objects.get(comment=comment,user=request.user)
                liked_comment.delete()
                return JsonResponse({'status': 'ok','action': 'Like'})
            except Like.DoesNotExist:
                like_comment = Like.objects.create(comment=comment,user=request.user)
                like_comment.save()
                #create_action(request.user, 'liked a comment on','comment', post)
                return JsonResponse({'status': 'ok','action': 'Unlike'})
    return JsonResponse({'status': 'error'})

# notification-actions
@login_required
@require_POST
def notification_action(request):
    action_id = request.POST.get('id')
    user_id = request.POST.get('user')
    choice = request.POST.get('action')
    action = Action.objects.get(id=action_id)
    user = User.objects.get(id=user_id)
    if user and action:
        if(choice == 'delete'):
            try:
                exist_action = UserAction.objects.get(user=request.user,action=action)
                UserAction.update_deleted(exist_action,True)
                return JsonResponse({'status': 'deleted','action': 'deleted'})
            except UserAction.DoesNotExist:
                user_action = UserAction(action=action,user=request.user,status='unread',deleted=True)
                user_action.save()
                return JsonResponse({'status': 'deleted','action': 'deleted'})
        if(choice == 'redo'):
            try:
                exist_action = UserAction.objects.get(user=request.user,action=action)
                UserAction.update_deleted(exist_action,False)
                return JsonResponse({'status': 'deleted','action': 'deleted'})
            except UserAction.DoesNotExist:
                pass
                #return JsonResponse({'status': 'deleted','action': 'deleted'})

        elif(choice == 'Unfollow'):
            try:
                user = User.objects.get(id=user_id)
                name = str(user.first_name).lower()
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
                create_action(request.user, 'unfollowed','follow', user)
                return JsonResponse({'status': 'unfollowed','user': f'{name}','action': 'Follow'})
            except User.DoesNotExist:
                return JsonResponse({'status':'error'})
        elif(choice == 'Follow'):
            try:
                user = User.objects.get(id=user_id)
                name = str(user.first_name).lower()
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, 'is following','follow', user)
                return JsonResponse({'status': 'followed','user':f'{name}' ,'action': 'Unfollow'})
            except User.DoesNotExist:
                return JsonResponse({'status':'error'})
        elif(choice == 'read'):
            try:
                exist_action = UserAction.objects.get(user=request.user,action=action)
                UserAction.update_status(exist_action,status='read')
                return JsonResponse({'status': 'unread','action': 'unread'})
            except UserAction.DoesNotExist:
                user_action = UserAction(action=action,user=request.user,status='read',deleted=False)
                user_action.save()
                return JsonResponse({'status': 'unread','action': 'unread'})

        elif(choice == 'unread'):
            try:
                exist_action = UserAction.objects.get(user=request.user,action=action)
                UserAction.update_status(exist_action,status='unread')
                return JsonResponse({'status': 'read','action': 'read'})
            except UserAction.DoesNotExist:
                user_action = UserAction(action=action,user=request.user,status='unread',deleted=False)
                user_action.save()
                #create_user_action(action=action,user=request.user,status='unread',deleted=False)
                return JsonResponse({'status': 'read','action': 'read'})
    return JsonResponse({'status': 'error'})


#Create
@login_required
def create_options(request):
    user = request.user

    # Display all actions by default
    total_posts = Post.published.filter(author=user).count()
    total_issues = Issue.published.filter(author=user).count()
    followers = user.followers.count()

    return render(request,
                 'editors/create-options.html',
                    {'total_posts':total_posts,
                    'total_issues':total_issues,
                    'followers':followers,
                    'title':'create',
                    'tab_c':'create',
                    'name':'publications',
                    'section':'create'})

@login_required
def create_post(request):
    user = request.user
    profile = user.profile
    post_form = None
    if request.method == 'POST':
        #Form is sent
        post_form = CreateBlogPostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            #Assign The Current User To the Post
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            tags = post_form.cleaned_data["tags"]
            text_tags = ",".join([str(tag).lower() for tag in tags])
            text_tags = text_tags.replace(" ","")
            text_tags = text_tags.replace("[","")
            text_tags = text_tags.replace("]","")

            post.tags.set(text_tags.split(","),clear=True)
            # post_form.save_m2m()
            create_action(request.user, 'added article','create', post)
            messages.success(request, 'Article was created')
            return HttpResponseRedirect(reverse('editors:user_post_list'))
        else:
            messages.error(request, 'Error! Article not created')
            post_form = CreateBlogPostForm(data=request.GET)
        return render(request,
                      'editors/articles/create.html',
                      {'post_form': post_form,
                       'user':user,
                       'profile':profile,
                       'section': 'article'})
    else:
        post_form = CreateBlogPostForm(data=request.GET)
        return render(request,
                      'editors/articles/create.html',
                      {'post_form': post_form,
                       'user':user,
                       'profile':profile,
                       'section': 'article'})

#Blog Posts Created By The Current User.
@login_required
def user_post_list(request):
    object_list = Post.published.filter(author=request.user)

    paginator = Paginator(object_list, 10) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/user_articles_list.html',
                  {'page': page,
                   'posts': posts,
                   'tab_c':'create',
                   'title': 'published',
                   'name':'publications',
                   'section': 'my-articles'})

#Blog Posts Created By The Current User.
@login_required
def user_drafted_list(request):
    object_list = Post.objects.filter(author=request.user,status='draft')

    paginator = Paginator(object_list, 10) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/user_articles_list.html',
                  {'page': page,
                   'posts': posts,
                   'title': 'drafted',
                   'tab_c':'create',
                   'name':'publications',
                   'section': 'my-articles'})


@login_required
def edit_blog_post(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditForm(request.POST or None, instance=post,files=request.FILES)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            title = cd['title']
            body = cd['body']
            status = cd['status']
            Post.update_post(post,title=title,body=body, status=status)
            #edit_form.save()
            messages.success(request, 'Post updated')
            return HttpResponseRedirect(reverse('editors:user_post_list'))

        else:
            messages.error(request, 'Error! updating')
            edit_form = BlogEditForm(request.POST or None, instance=post,files=request.FILES)

        return render(request,
                        'editors/articles/edit.html',
                        {'edit_form': edit_form,
                         'user':user,
                         'profile':profile,
                         'section': 'article'})
    else:
        edit_form = BlogEditForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/edit.html',
                        {'edit_form': edit_form,
                         'user':user,
                         'profile':profile,
                         'section': 'article'})

#Edit Articles Tags
@login_required
def edit_article_tags(request, pk):
    #post = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        tags = request.POST.get("tags")
        tags.replace(" ","")
        text_tags = tags.lower()
        post.tags.set(text_tags.split(","),clear=True)
        messages.success(request, 'Tags updated')
        return HttpResponseRedirect(reverse('editors:user_post_list'))
    else:
        messages.error(request, 'Error updating!')


#Edit Article Cover Photo
@login_required
def edit_article_cover(request, pk):
    #post = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        cover = request.FILES.get("photo")
        Post.update_cover(post,cover)
        messages.success(request, 'Cover updated')
        return HttpResponseRedirect(reverse('editors:user_post_list'))

    else:
        messages.error(request, 'Error updating!')


# process delete post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    messages.success(request, 'Article deleted')
    return HttpResponseRedirect(reverse('editors:user_post_list'))

#Themes
@login_required
def theme_list(request):
    object_list = Theme.objects.all()

    paginator = Paginator(object_list, 10) # 5 posts in each page
    page = request.GET.get('page')
    try:
        themes = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        themes = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        themes = paginator.page(paginator.num_pages)

    return render(request, 'editors/themes/themes.html',
                  {'page': page,
                   'themes': themes,
                   'title': 'explore',
                   'section': 'themes'})

# notification-actions
@login_required
@require_POST
def use_theme(request):
    theme_id = request.POST.get('id')
    user_id = request.POST.get('user')
    theme = Theme.objects.get(id=theme_id)
    user = User.objects.get(id=user_id)
    if user and theme:
        try:
            user_theme = UserTheme.objects.get(user=user)
            UserTheme.update_user_theme(user_theme,theme=theme,user=user)
            Theme.update_users(theme)
            # request.session['preferences'] = theme.preferences
            return JsonResponse(theme.preferences)
        except UserTheme.DoesNotExist:
            UserTheme.objects.create(theme=theme,user=user)
            Theme.update_users(theme)
            # request.session['preferences'] = theme.preferences
            return JsonResponse(theme.preferences)
    return JsonResponse({'status': 'error'})


#Create Magazine View
#@login_required
@login_required
def create_magazine(request):
    magazine_form = None
    #magazine_form = None
    if request.method == 'POST':
        #Form is sent
        magazine_form = CreateMagazineForm(data=request.POST,files=request.FILES)
        if magazine_form.is_valid():
            issue = magazine_form.save(commit=False)
            issue.author = request.user
            issue.save()
            magazine_form.save_m2m()
            #Assign The Current User To the Post
            #new_magazine.author = request.user
            #new_magazine.tags = cd['tags']
            #new_magazine.save()
            messages.success(request, 'Newsletter created')
            return HttpResponseRedirect(reverse('editors:user_issue_list'))
        else:
            messages.error(request, 'Error! Newsletter not created')
            magazine_form = CreateMagazineForm(data=request.POST)
        return render(request,
                      'editors/articles/create-magazine.html',
                      {'magazine_form': magazine_form})
    else:
        magazine_form = CreateMagazineForm(data=request.POST)
        return render(request,
                      'editors/articles/create-magazine.html',
                      {'magazine_form': magazine_form,
                       'section': 'issue'})

#Newsletter created by The Current User.
#@login_required
@login_required
def user_issue_list(request):
    user = request.user
    profile = user.profile
    object_list = Issue.published.all().filter(author=request.user)

    paginator = Paginator(object_list, 3) # 5 issues in each page
    page = request.GET.get('page')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        issues = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/user_issues_list.html',
                  {'page': page,
                   'issues': issues,
                   'user': user,
                   'profile': profile,
                   'section': 'issue-list'})

#Edit Magazine Newsletter
@login_required
def edit_newsletter(request, pk):
    #post = get_object_or_404(Post, id=pk)
    issue = Issue.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = MagazineEditForm(request.POST or None, instance=issue,
                                     files=request.FILES)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            no = cd['no']
            title = cd['title']
            description = cd['description']
            status = cd['status']
            Issue.update_issue(issue,no,title,description,status)
            messages.success(request, 'Newsletter updated')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating Newsletter!')
            edit_form = MagazineEditForm(request.POST or None, instance=issue,
                                         files=request.FILES)

        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form,
                         'section':'issue'})
    else:
        edit_form = MagazineEditForm(request.POST or None,
                                     instance=issue)
        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form,
                         'section':'issue'})

#Edit Magazine Newsletter Tags
#@login_required
@login_required
def edit_newsletter_tags(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    issue = Issue.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = MagazineEditTagsForm(request.POST or None, instance=issue)
        if edit_form.is_valid():
            tags = edit_form.save(commit=False)
            edit_form.save_m2m()
            tags.save()
            messages.success(request, 'Tags updated')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating tags')
            edit_form = MagazineEditTagsForm(request.POST or None, instance=issue)

        return render(request,
                        'editors/articles/issue-tags-edit.html',
                        {'edit_form': edit_form,
                         'issue': issue,
                         'user':user,
                         'profile':profile,
                         'section': 'issue-list'})
    else:
        edit_form = MagazineEditTagsForm(request.POST or None, instance=issue)
        return render(request,
                        'editors/articles/issue-tags-edit.html',
                        {'edit_form': edit_form,
                         'issue': issue,
                         'user':user,
                         'profile':profile,
                         'section': 'issue-list'})

#Edit Issue Cover Photo
@login_required
def edit_newsletter_cover(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    issue = Issue.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = MagazineEditCoverForm(request.POST or None, instance=issue,files=request.FILES)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            cover = cd['cover']
            #edit_form.save()
            Issue.update_cover(issue,cover)
            messages.success(request, 'Cover updated')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating cover')
            edit_form = MagazineEditCoverForm(request.POST or None, instance=issue, files=request.FILES)

        return render(request,
                        'editors/articles/edit-issue-cover.html',
                        {'edit_form': edit_form,
                         'user':user,
                         'profile':profile,
                         'section': 'issue-list'})
    else:
        edit_form = MagazineEditCoverForm(request.POST or None, instance=issue)
        return render(request,
                        'editors/articles/edit-issue-cover.html',
                        {'edit_form': edit_form,
                         'issue': issue,
                         'user':user,
                         'profile':profile,
                         'section': 'issue-list'})


#Deleting an Issue
#@login_required
@login_required
def delete_issue(request, pk):
    post = get_object_or_404(Issue, id=pk)
    post.delete()
    messages.success(request, 'Newsletter deleted')
    return HttpResponseRedirect(reverse('user_issue_list'))
