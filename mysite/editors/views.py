from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CreateBlogPostForm,\
        BlogEditForm
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Profile
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


# Create your views here.
@login_required
def dashboard(request):
    return render(request,
                  'editors/dashboard.html',
                  {'section': dashboard})

#Registration View
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Create a new user object but we don't save it yet
            new_user = user_form.save(commit=False)
            #Setting the password
            new_user.set_password(
                user_form.cleaned_data['password'])
            #Saving The User Object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'editors/register_done.html',
                          {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
        return render(request,
                      'editors/register.html',
                      {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'editors/register.html',
                      {'user_form': user_form})

#Edit User Info
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(request, 'Error updating your profile')
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'editors/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'editors/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

@login_required
def create_post(request):
    post_form = None
    if request.method == 'POST':
        #Form is sent
        post_form = CreateBlogPostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            #Assign The Current User To the Post
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Your Post Was added')
        else:
            post_form = CreateBlogPostForm(data=request.GET)
        return render(request,
                      'editors/articles/create.html',
                      {'post_form': post_form})
    else:
        post_form = CreateBlogPostForm(data=request.GET)
        return render(request,
                      'editors/articles/create.html',
                      {'post_form': post_form})


#Blog Posts Created By The Current User.
@login_required
def user_post_list(request):
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
                   'posts': posts,})

@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    #post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditForm(request.POST or None, instance=post)
        if edit_form.is_valid():
            edited = edit_form.save()
            messages.success(request, 'Post updated successfully')
            return HttpResponseRedirect(reverse('user_post_list'))

        else:
            messages.error(request, 'Error updating the Post')
            edit_form = BlogEditForm(request.POST or None, instance=post)

        return render(request,
                        'editors/articles/edit.html',
                        {'edit_form': edit_form})
    else:
        edit_form = BlogEditForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/edit.html',
                        {'edit_form': edit_form})


# process delete post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()

    if(request.user.is_staff):
        return HttpResponseRedirect(reverse('backend:posts'))
    else:
        return HttpResponseRedirect(reverse('backend:posts_by_author'))
