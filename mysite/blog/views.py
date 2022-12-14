from re import search
from unittest import result
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import EmailPostForm,BlogCommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from actions.utils import create_action
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag,})

#Class based View
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, username,month, day, slug):
    user = User.objects.get(username=username)
    post = get_object_or_404(Post, slug=slug, status='published',
                             author=user,
                             publish__month=month,
                             publish__day=day)

    #Update Views count on each visit
    if post:
        post.update_views()
    #List of active comments for this post
    comments = post.comments.filter(active=True).order_by('-created')

    new_comment = None
    comment_form = None
    if user.is_authenticated:
        if request.method == 'POST':
            #A Comment was posted
            comment_form = BlogCommentForm(data=request.POST)
            if comment_form.is_valid():
                #Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                #Assign the current post and user to comment
                new_comment.post = post
                new_comment.author = request.user
                #Save the comment to the database
                new_comment.save()
                create_action(request.user, 'commented on','comment', post)
                messages.success(request, 'Comment was added')
            else:
                comment_form = BlogCommentForm()
                messages.error(request, 'Error! Comment was not added')
        else:
            comment_form = BlogCommentForm()

    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,
                   'section':'read',
                   'title':'article',
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})



def post_share(request, post_id):
    #Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            #...Send Email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post':post,
                                                    'form':form,
                                                    'sent':sent})

