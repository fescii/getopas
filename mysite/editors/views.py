from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login

from magazine.models import Issue, Section
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CreateBlogPostForm,\
        BlogEditForm, CreateMagazineForm, MagazineEditForm,\
            CreateSectionForm
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
            return HttpResponseRedirect(reverse('dashboard'))

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
            return HttpResponseRedirect(reverse('user_post_list'))
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
    #post = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditForm(request.POST or None, instance=post)
        if edit_form.is_valid():
            edit_form.save()
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
    messages.success(request, 'Post deleted successfully')
    return HttpResponseRedirect(reverse('user_post_list'))

#Create Magazine View
@login_required
def create_magazine(request):
    magazine_form = None
    #magazine_form = None
    if request.method == 'POST':
        #Form is sent
        magazine_form = CreateMagazineForm(data=request.POST)
        if magazine_form.is_valid():
            cd = magazine_form.cleaned_data
            no = cd['no']
            title = cd['title']
            author = request.user
            description = cd['description']
            status = cd['status']
            tags = cd['tags']
            new = Issue(no=no,
                        title=title,
                        author=author,
                        description=description,
                        status=status,
                        tags=tags)
            #Assign The Current User To the Post
            #new_magazine.author = request.user
            #new_magazine.tags = cd['tags']
            #new_magazine.save()
            new.save()
            messages.success(request, f'Magazine Was {magazine_form.cleaned_data}Created Successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))
        else:
            magazine_form = CreateMagazineForm(data=request.GET)
        return render(request,
                      'editors/articles/create-magazine.html',
                      {'magazine_form': magazine_form})
    else:
        magazine_form = CreateMagazineForm(data=request.GET)
        return render(request,
                      'editors/articles/create-magazine.html',
                      {'magazine_form': magazine_form})

#Newsletter created by The Current User.
@login_required
def user_issue_list(request):
    object_list = Issue.published.all().filter(author=request.user)

    paginator = Paginator(object_list, 5) # 5 issues in each page
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
                   'issues': issues,})
#Edit Magazine Newsletter
@login_required
def edit_newsletter(request, pk):
    #post = get_object_or_404(Post, id=pk)
    post = Issue.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = MagazineEditForm(request.POST or None, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Issue updated successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating the Issue')
            edit_form = MagazineEditForm(request.POST or None, instance=post)

        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form})
    else:
        edit_form = MagazineEditForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form})

#Deleting an Issue
@login_required
def delete_issue(request, pk):
    post = get_object_or_404(Issue, id=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully')
    return HttpResponseRedirect(reverse('user_issue_list'))


#List Newsletter By The User.
@login_required
def user_issue_section_list(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    sections = issue.sections.all()
    """
    paginator = Paginator(sections, 5) # 5 issues in each page
    page = request.GET.get('page')
    try:
        sections = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        sections = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        sections = paginator.page(paginator.num_pages)
    """
    return render(request, 'editors/articles/user_issues_sections.html',
                  {'sections': sections,
                   'obj': issue})

#Edit Newsletter Section
@login_required
def create_section(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    section_form = None
    if request.method == 'POST':
        #Form is sent
        section_form = CreateSectionForm(data=request.POST)
        if section_form.is_valid():
            new_section = section_form.save(commit=False)
            #Assign The Current Issue To the Section
            new_section.issue = pk
            new_section.save()
            messages.success(request, 'Your Section Was added Successfully')
            #return HttpResponseRedirect(reverse('user_post_list'))
        else:
            section_form = CreateSectionForm(data=request.GET)
        return render(request,
                      'editors/articles/create-section.html',
                      {'post_form': section_form,
                       'issue':issue})
    else:
        section_form = CreateSectionForm(data=request.GET)
        return render(request,
                      'editors/articles/create-section.html',
                      {'post_form': section_form,
                       'issue':issue})
