from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login

from magazine.models import Issue, Section
from devices.models import Product,PhysicalInfo, SoftwareInfo, Review, Image
from .forms import  CreateBlogPostForm,\
        BlogEditForm, CreateMagazineForm, MagazineEditForm,\
            CreateSectionForm, SectionEditForm, MagazineEditTagsForm,\
                BlogEditTagsForm, BlogEditCoverForm,\
                    MagazineEditCoverForm
from devices.forms import CreateProductForm, EditProductForm, EditProductTags,\
    EditPhysicalInfo, EditSoftwareInfo, CreatePhysicalInfo, CreateSoftwareInfo,\
        AddProductPhoto, EditProductCover
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from account.views import is_admin, is_editor, is_author
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from account.models import Profile
from blog.models import Post,Bookmark
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from taggit.models import Tag
from actions.utils import create_action
from actions.models import Action
from account.models import Contact


# Create your views here.

#Dashboard
@login_required
def dashboard(request):
    user = request.user
    profile = user.profile

    # Display all actions by default
    posts_interest = Post.objects.exclude(author=request.user)
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
                    'title':'home',
                    'section':'opas'})

#Dashboard
@login_required
def explore(request,topic=None):
    user = request.user
    profile = user.profile

    #Getting Total articles views and comments of the current user
    object_list = Post.published.all()
    tag = None
    if topic:
        tag = get_object_or_404(Tag, slug=topic)
        topic_posts = object_list.filter(tags__in=[tag])

    paginator = Paginator(topic_posts, 8) # 5 posts in each page
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
                 'editors/explore.html',
                    {'user': user,
                    'profile': profile,
                    'topic': topic,
                    'section': 'explore',
                    'title': 'explore',
                    'topic_posts': posts})

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
                  {'title': 'feeds',
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
                  {'title': 'topics',
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
                  {'title': 'interests',
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
                  {'title': 'trending',
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
                  {'title': 'recent',
                   'section': 'articles',
                   'posts': posts})


#Actions.
@login_required
def actions(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')

    paginator = Paginator(actions, 12)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)
    return render(request,
                  'editors/actions.html',
                  {'section': 'notifications',
                   'title': 'notifications',
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
                    'title': 'My List',
                    'section': 'my-list'})

#Add-Post-To-My-list
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
                create_action(request.user, 'remove from saved','remove', post)
                return JsonResponse({'status': 'ok','action': 'Save'})
            except Bookmark.DoesNotExist:
                bookmark = Bookmark.objects.create(post=post,user=request.user)
                bookmark.save()
                create_action(request.user, 'saved article','save', post)
                return JsonResponse({'status': 'ok','action': 'Remove'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

#   Add-Post-To-My-list
@login_required
@require_POST
def notification_action(request):
    action_id = request.POST.get('id')
    action = request.POST.get('action')
    user_id = request.POST.get('user')
    if action_id and action:
        if(action == 'delete'):
            try:
                action = Action.objects.get(id=action_id)
                action.delete()
                #messages.success(request, 'Notification deleted successfully')
                return JsonResponse({'status': 'deleted','action': 'deleted'})
            except Action.DoesNotExist:
                pass
        elif(action == 'Unfollow'):
            try:
                user = User.objects.get(id=user_id)
                name = str(user.first_name).lower()
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
                create_action(request.user, 'unfollowed','follow', user)
                return JsonResponse({'status': 'unfollowed','user': f'{name}','action': 'Follow'})
            except User.DoesNotExist:
                return JsonResponse({'status':'error'})
        elif(action == 'Follow'):
            try:
                user = User.objects.get(id=user_id)
                name = str(user.first_name).lower()
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, 'is following','follow', user)
                return JsonResponse({'status': 'followed','user':f'{name}' ,'action': 'Unfollow'})
            except User.DoesNotExist:
                return JsonResponse({'status':'error'})
        elif(action == 'read'):
            action = Action.objects.get(id=action_id)
            try:
                Action.update_status(action,status='read')
                return JsonResponse({'status': 'unread','action': 'unread'})
            except:
                pass
        elif(action == 'unread'):
            action = Action.objects.get(id=action_id)
            try:
                Action.update_status(action,status='unread')
                return JsonResponse({'status': 'read','action': 'read'})
            except:
                pass
    return JsonResponse({'status': 'error'})

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
            post_form.save_m2m()
            create_action(request.user, 'added article','create', post)
            messages.success(request, 'Blog Post Created Successfully')
            return HttpResponseRedirect(reverse('editors:user_post_list'))
        else:
            messages.error(request, 'Error! Blog post was not created')
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
    user = request.user
    profile = user.profile
    object_list = Post.published.all().filter(author=request.user)

    paginator = Paginator(object_list, 5) # 5 posts in each page
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
                   'user':user,
                   'profile':profile,
                   'section': 'article-list'})
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
            messages.success(request, 'Post updated successfully')
            return HttpResponseRedirect(reverse('user_post_list'))

        else:
            messages.error(request, 'Error updating the Post')
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
def edit_blog_post_tags(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditTagsForm(request.POST or None, instance=post)
        if edit_form.is_valid():
            tags = edit_form.save(commit=False)
            edit_form.save_m2m()
            tags.save()
            messages.success(request, 'Tags updated successfully')
            return HttpResponseRedirect(reverse('editors:user_post_list'))

        else:
            messages.error(request, 'Error updating the Tags')
            edit_form = BlogEditTagsForm(request.POST or None, instance=post)

        return render(request,
                        'editors/articles/edit-post-tags.html',
                        {'edit_form': edit_form,
                         'user':user,
                         'profile':profile,
                         'section': 'article-list'})
    else:
        edit_form = BlogEditTagsForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/edit-post-tags.html',
                        {'edit_form': edit_form,
                         'post': post,
                         'user':user,
                         'profile':profile,
                         'section': 'article-list'})

#Edit Article Cover Photo
@login_required
def edit_blog_post_cover(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditCoverForm(request.POST or None, instance=post,files=request.FILES)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            cover = cd['cover']
            #edit_form.save()
            Post.update_cover(post,cover)
            messages.success(request, 'Cover updated successfully')
            return HttpResponseRedirect(reverse('editors:user_post_list'))

        else:
            messages.error(request, 'Error updating the Tags')
            edit_form = BlogEditCoverForm(request.POST or None, instance=post, files=request.FILES)

        return render(request,
                        'editors/articles/edit-post-cover.html',
                        {'edit_form': edit_form,
                         'user':user,
                         'post': post,
                         'profile':profile,
                         'section': 'article-list'})
    else:
        edit_form = BlogEditCoverForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/edit-post-cover.html',
                        {'edit_form': edit_form,
                         'post': post,
                         'user':user,
                         'profile':profile,
                         'section': 'article-list'})

# process delete post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    messages.success(request, 'Article deleted successfully')
    return HttpResponseRedirect(reverse('editors:user_post_list'))

#Create Magazine View
#@login_required
@user_passes_test(is_editor)
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
            messages.success(request, 'Magazine issue was created Successfully')
            return HttpResponseRedirect(reverse('editors:user_issue_list'))
        else:
            messages.error(request, 'Error! Magazine issue was not created')
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
@user_passes_test(is_editor)
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
@user_passes_test(is_editor)
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
            messages.success(request, 'Issue updated successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating the Issue')
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
@user_passes_test(is_editor)
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
            messages.success(request, 'Tags updated successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating the Tags')
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
@user_passes_test(is_editor)
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
            messages.success(request, 'Cover updated successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating the cover')
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
@user_passes_test(is_editor)
def delete_issue(request, pk):
    post = get_object_or_404(Issue, id=pk)
    post.delete()
    messages.success(request, 'Issue deleted successfully')
    return HttpResponseRedirect(reverse('user_issue_list'))


#List Newsletter By The User.
#@login_required
@user_passes_test(is_editor)
def user_issue_section_list(request, pk):
    user = request.user
    profile = user.profile
    issue = get_object_or_404(Issue, id=pk)
    all_sections = issue.sections.all().order_by('-page')

    paginator = Paginator(all_sections, 5) # 5 sections in each page
    page = request.GET.get('page')
    try:
        sections = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        sections = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        sections = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/user_issues_sections.html',
                  {'sections': sections,
                   'issue': issue,
                   'section': 'issue-list',
                   'user': user,
                   'profile': profile})

#Edit Newsletter Section
@user_passes_test(is_editor)
def create_section(request, pk):
    issue = Issue.objects.get(id=pk)
    user = request.user
    profile =  user.profile
    if request.method == 'POST':
        #Form is sent
        section_form = CreateSectionForm(data=request.POST)
        if section_form.is_valid():
            new_section = section_form.save(commit=False)
            #Assign The Current Issue To the Section
            new_section.issue = issue
            new_section.save()
            messages.success(request, 'Your Section Was added Successfully')
            return HttpResponseRedirect(reverse('editors:user_issue_section_list',kwargs={'pk': pk}))
        else:
            messages.error(request, 'Error! Issue Section was not created')
            section_form = CreateSectionForm(data=request.GET)
        return render(request,
                      'editors/articles/create-section.html',
                      {'post_form': section_form,
                       'issue':issue,
                       'section': 'create-section',
                       'user': user,
                       'profile':profile})
    else:
        section_form = CreateSectionForm(data=request.GET)
        return render(request,
                      'editors/articles/create-section.html',
                      {'post_form': section_form,
                       'issue':issue,
                       'section': 'create-section',
                       'user': user,
                       'profile':profile})


# Add Section To Issue
#@login_required
@user_passes_test(is_editor)
def add_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.added = True
    section.save()
    messages.success(request, 'Section added')
    return HttpResponseRedirect(reverse('editors:user_issue_section_list',kwargs={'pk': issue_id}))

# Remove Section From An Issue
#@login_required
@user_passes_test(is_editor)
def remove_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.added = False
    section.save()
    messages.success(request, 'Section was removed')
    return HttpResponseRedirect(reverse('editors:user_issue_section_list', kwargs={'pk': issue_id}))

# Delete Section
#@login_required
@user_passes_test(is_editor)
def delete_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    messages.success(request, 'Section was deleted')
    return HttpResponseRedirect(reverse('editors:user_issue_section_list',kwargs={'pk': issue_id}))

#Edit Edit Section
#@login_required
@user_passes_test(is_editor)
def edit_section(request, issue_id, section_id):
    issue = Issue.objects.get(id=issue_id)
    user = request.user
    profile =  user.profile
    section = Section.objects.get(id=section_id)
    section_edit_form = SectionEditForm(request.POST or None, instance=section)
    if request.method == 'POST':
        section_edit_form = SectionEditForm(request.POST or None, instance=section)
        if section_edit_form.is_valid():
            section_edit_form.save()
            messages.success(request, 'Section updated successfully')
            return HttpResponseRedirect(reverse('editors:user_issue_section_list',kwargs={'pk': issue_id}))

        else:
            messages.error(request, 'Error updating the Section')
            section_edit_form = SectionEditForm(request.POST, instance=section)

        return render(request,
                        'editors/articles/section-edit.html',
                        {'section_edit_form': section_edit_form,
                        'issue': issue,
                        'section': 'create-section',
                        'user':user,
                        'profile': profile})
    else:
        return render(request,
                        'editors/articles/section-edit.html',
                        {'section_edit_form': section_edit_form,
                        'issue': issue,
                        'section': 'create-section',
                        'user': user,
                        'profile': profile})


#List Users Products
@user_passes_test(is_editor)
def user_product_list(request):
    user = request.user
    profile = user.profile
    object_list = Product.published.all().filter(author=request.user).order_by('-release_date')

    paginator = Paginator(object_list, 5) # 5 issues in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request, 'editors/products/list-user-products.html',
                  {'page': page,
                   'products': products,
                   'user': user,
                   'profile': profile,
                   'section': 'devices'})


#Creating a new product
@user_passes_test(is_editor)
def create_product(request):
    user = request.user
    profile = user.profile
    product_form = CreateProductForm()
    if request.method == 'POST':
        product_form = CreateProductForm(request.POST, files=request.FILES)
        if product_form.is_valid():
            cd = product_form.cleaned_data
            name = cd['name']
            new_product = product_form.save(commit=False)
            new_product.author = request.user
            new_product.save()
            product_form.save_m2m()
            messages.success(request, f'The Product {name} was created successfully')
            return HttpResponseRedirect(reverse('editors:user_product_list'))
        else:
            messages.error(request, 'An error occurred, Please try again!')
            product_form = CreateProductForm()
            return render(request,
                          'editors/products/create-product.html',
                          {'product_form': product_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user})
    else:
        product_form = CreateProductForm()
        return render(request,
                      'editors/products/create-product.html',
                          {'product_form': product_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user})

#Edit Issue Cover Photo
@login_required
def edit_product_cover(request, pk):
    #post = get_object_or_404(Post, id=pk)
    user = request.user
    profile = user.profile
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = EditProductCover(request.POST or None, instance=product,files=request.FILES)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            cover = cd['cover']
            #edit_form.save()
            Product.update_cover(product,cover)
            messages.success(request, 'Cover updated successfully')
            return HttpResponseRedirect(reverse('editors:user_product_list'))

        else:
            messages.error(request, 'Error updating the cover')
            edit_form = EditProductCover(request.POST or None, instance=product, files=request.FILES)

        return render(request,
                        'editors/products/edit-product-cover.html',
                        {'edit_form': edit_form,
                         'product': product,
                         'section': 'devices-create',
                         'user': user,
                         'profile': profile})
    else:
        edit_form = EditProductCover(request.POST or None, instance=product)
        return render(request,
                        'editors/products/edit-product-cover.html',
                        {'edit_form': edit_form,
                         'product': product,
                         'section': 'devices-create',
                         'user': user,
                         'profile': profile})

#Editing a product
@user_passes_test(is_editor)
def edit_product(request, product_id, product_name):
    user = request.user
    profile = user.profile
    product = Product.objects.get(id=product_id)
    product_name = product.name
    product_form = EditProductForm(request.POST or None, instance=product)
    if request.method == 'POST':
        product_form = EditProductForm(request.POST or None, instance=product,
                                     files=request.FILES)
        if product_form.is_valid():
            cd = product_form.cleaned_data
            Product.update_product(product, cd['title'], cd['name'],
                                   cd['model'],cd['series'],
                                   cd['company'], cd['release_date'], cd['price'],
                                   cd['about'])
            messages.success(request, f"The Product was updated successfully")
            return HttpResponseRedirect(reverse('editors:user_product_list'))
        else:
            messages.error(request, 'An error occurred, Please try again!')
            product_form = EditProductForm(request.POST or None, instance=product,
                                     files=request.FILES)
            return render(request,
                          'editors/products/edit-product.html',
                          {'product_form': product_form,
                          'name': product_name,
                          'section': 'devices-create',
                           'profile': profile,
                           'user': user})
    else:
        return render(request,
                      'editors/products/edit-product.html',
                          {'product_form': product_form,
                           'name': product_name,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user})

#Edit Products Tags
@user_passes_test(is_editor)
def edit_product_tags(request, product_id, product_name):
    user = request.user
    profile = user.profile
    product = Product.objects.get(id=product_id)
    product_name = product.name
    if request.method == 'POST':
        edit_form = EditProductTags(request.POST or None, instance=product)
        if edit_form.is_valid():
            tags = edit_form.save(commit=False)
            edit_form.save_m2m()
            tags.save()
            messages.success(request, 'Product Tags updated successfully')
            return HttpResponseRedirect(reverse('editors:user_product_list'))

        else:
            messages.error(request, 'Error updating the Tags')
            edit_form = EditProductTags(request.POST or None, instance=product)

        return render(request,
                        'editors/products/edit-product-tags.html',
                        {'edit_form': edit_form,
                         'name': product_name,
                         'section': 'devices-create',
                         'user': user,
                         'profile': profile})
    else:
        edit_form = EditProductTags(request.POST or None, instance=product)
        return render(request,
                        'editors/products/edit-product-tags.html',
                        {'edit_form': edit_form,
                         'name': product_name,
                         'section': 'devices-create',
                         'user': user,
                         'profile': profile})

#Viewing Physical Information of a  product
@user_passes_test(is_editor)
def show_physical_info(request, pk):
    user = request.user
    profile = user.profile
    product = get_object_or_404(Product, id=pk)

    #Get The product Physical Information
    info = PhysicalInfo.get_physical(PhysicalInfo, product)
    return render(request, 'editors/products/physical-product-info.html',
                  {'physical_info': info,
                   'product': product,
                   'section': 'devices-info',
                   'user': user,
                   'profile': profile})

#Viewing Physical Information of a  product
@user_passes_test(is_editor)
def show_software_info(request, pk):
    user = request.user
    profile = user.profile
    product = get_object_or_404(Product, id=pk)

    #Get The product Physical Information
    info = SoftwareInfo.get_software(SoftwareInfo, product)

    return render(request, 'editors/products/software-product-info.html',
                  {'software_info': info,
                   'product': product,
                   'section': 'devices-info',
                   'user': user,
                   'profile': profile})


# Adding Physical Information of a  product if no present
@user_passes_test(is_editor)
def add_physical_info(request, pk):
    user = request.user
    profile = user.profile
    info_form = CreatePhysicalInfo()
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        info_form = CreatePhysicalInfo(request.POST)
        if info_form.is_valid():
            cd = info_form.cleaned_data
            new_info = info_form.save(commit=False)
            new_info.product = product
            new_info.save()
            info_form.save_m2m()
            messages.success(request, f'Physical information was added successfully')
            return HttpResponseRedirect(reverse('editors:user_product_list'))
        else:
            messages.error(request, 'An error occurred, Please try again!')
            info_form = CreatePhysicalInfo()
            return render(request,
                          'editors/products/create-physical-info.html',
                          {'info_form': info_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user})
    else:
        info_form = CreatePhysicalInfo()
        return render(request,
                      'editors/products/create-physical-info.html',
                          {'info_form': info_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user})

# Adding Physical Information of a  product if no present
@user_passes_test(is_editor)
def add_software_info(request, pk):
    user = request.user
    profile = user.profile
    info_form = CreateSoftwareInfo()
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        info_form = CreateSoftwareInfo(request.POST)
        if info_form.is_valid():
            cd = info_form.cleaned_data
            new_info = info_form.save(commit=False)
            new_info.product = product
            new_info.save()
            info_form.save_m2m()
            messages.success(request, f'Software information for  was added successfully')
            return HttpResponseRedirect(reverse('editors:user_product_list'))
        else:
            messages.error(request, 'An error occurred, Please try again!')
            info_form = CreateSoftwareInfo()
            return render(request,
                          'editors/products/create-software-info.html',
                          {'info_form': info_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})
    else:
        info_form = CreateSoftwareInfo()
        return render(request,
                      'editors/products/create-software-info.html',
                          {'info_form': info_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})


@user_passes_test(is_editor)
def edit_physical_info(request, info_id, product_id):
    user = request.user
    profile = user.profile
    physical = get_object_or_404(PhysicalInfo, id=info_id)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        physical_form = EditPhysicalInfo(request.POST, instance=physical)

        if physical_form.is_valid():
            cd = physical_form.cleaned_data
            #Saving The Form
            updated = physical_form.save(commit=False)
            updated.save()
            physical_form.save_m2m()
            #On Success
            messages.success(request,'Physical Information updated successfully')
            return HttpResponseRedirect(reverse('editors:product_physical_info', kwargs={'pk': product_id}))
        else:
            messages.error(request,'An error occurred, Please Try again')
            physical_form = EditPhysicalInfo(request.POST or None, instance=physical)
            return render(request, 'editors/products/edit-physical-info.html',
                          {'physical_form': physical_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})
    else:
        physical_form = EditPhysicalInfo(request.POST or None, instance=physical)
        return render(request, 'editors/products/edit-physical-info.html',
                          {'physical_form': physical_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})

#Editing Software Info
@user_passes_test(is_editor)
def edit_software_info(request, info_id, product_id):
    user = request.user
    profile = user.profile
    software = get_object_or_404(SoftwareInfo, id=info_id)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        software_form = EditSoftwareInfo(request.POST, instance=software)

        if software_form.is_valid():
            cd = software_form.cleaned_data

            #Saving The Form
            updated = software_form.save(commit=False)
            updated.save()
            software_form.save_m2m()

            #On Success
            messages.success(request,'Software Information updated successfully')
            return HttpResponseRedirect(reverse('editors:product_software_info', kwargs={'pk': product_id}))
        else:
            messages.error(request,'An error occurred, Please Try again')
            physical_form = EditSoftwareInfo(request.POST or None, instance=software)
            return render(request, 'editors/products/edit-software-info.html',
                          {'software_form': physical_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})
    else:
        physical_form = EditSoftwareInfo(request.POST or None, instance=software)
        return render(request, 'editors/products/edit-software-info.html',
                          {'software_form': physical_form,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})

#Delete Product
@user_passes_test(is_editor)
def delete_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Product was Successfully')
    return HttpResponseRedirect(reverse('editors:user_product_list'))


#Viewing Images of  product
@user_passes_test(is_editor)
def show_product_images(request, pk):
    user = request.user
    profile = user.profile
    product = get_object_or_404(Product, id=pk)

    #Get The product Physical Information
    images = Image.product_images_all(Image, product)

    return render(request, 'editors/products/show-product-images.html',
                  {'images': images,
                   'product': product,
                   'user': user,
                   'profile': profile,
                   'section': 'devices'})

# Add product image present
@user_passes_test(is_editor)
def add_image(request, product_id):
    user = request.user
    profile = user.profile
    image_form = AddProductPhoto(files=request.FILES)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        image_form = AddProductPhoto(request.POST,files=request.FILES)
        if image_form.is_valid():
            new_info = image_form.save(commit=False)
            new_info.product = product
            new_info.save()
            image_form.save_m2m()
            messages.success(request, 'Image was added successfully')
            return HttpResponseRedirect(reverse('editors:images', kwargs={'pk': product_id}))
        else:
            messages.error(request, 'An error occurred, Please try again!')
            image_form = AddProductPhoto(files=request.FILES)
            return render(request,
                          'editors/products/add-product-image.html',
                          {'info_form': info_form,
                           'product': product,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})
    else:
        info_form = AddProductPhoto(files=request.FILES)
        return render(request,
                      'editors/products/add-product-image.html',
                          {'image_form': image_form,
                           'product':product,
                           'section': 'devices-create',
                           'profile': profile,
                           'user': user,
                           'product': product})

#Delete Product image
@user_passes_test(is_editor)
def delete_image(request,product_id, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    messages.success(request, 'Image deleted successfully')
    return HttpResponseRedirect(reverse('editors:images', kwargs={'pk': product_id}))

#Most Viewed Newsletters
@login_required
def top_newsletters(request):
    user = request.user
    profile = user.profile
    #Top 30 Newsletters
    top_issues = Issue.published.order_by('-issue_views')[:30]

    paginator = Paginator(top_issues, 5) # 5 newsletters in each page
    page = request.GET.get('page')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        issues = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/top-newsletters.html',
                  {'page': page,
                   'issues': issues,
                   'user':user,
                   'profile':profile,
                   'section': 'issue-list'})

#Recent Articles
@login_required
def new_articles(request):
    user = request.user
    profile = user.profile
    #30 most recent articles
    recent_articles = Post.published.order_by('-publish')[:30]

    paginator = Paginator(recent_articles, 5) # 5 newsletters in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)

    return render(request, 'editors/articles/recent-articles.html',
                  {'page': page,
                   'posts': articles,
                   'user':user,
                   'profile':profile,
                   'section': 'article-list'})
