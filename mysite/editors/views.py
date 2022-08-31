from distutils.log import error
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login

from magazine.models import Issue, Section
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CreateBlogPostForm,\
        BlogEditForm, CreateMagazineForm, MagazineEditForm,\
            CreateSectionForm, SectionEditForm, MagazineEditTagsForm,\
                BlogEditTagsForm, ModerateUserForm
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Profile
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


# Create your views here.
#verify if an user is an admin
def is_admin(user):
    return user.is_superuser and user.is_staff

# verify if an user is a moderator
def is_moderator(user):
    return user.is_staff

# verify if an user is an author
def is_author(user):
    return user.is_active and not user.is_staff

#List Users
@user_passes_test(is_admin)
def list_users(request):
    users = User.objects.all()
    return render(request,
                  'editors/admin/users.html',
                  {'users': users,})

# modify an user based on action
@user_passes_test(is_admin)
def moderate_user(request, pk):
    form = ModerateUserForm()
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        if form.is_valid():
            cd = form.cleaned_data
            action = cd['role']

            if action == "admin":
                user.is_superuser = True
                user.is_staff = True
                user.save()

            elif action == "editor":
                user.is_superuser = False
                user.is_staff = True
                user.save()


            elif action == "author":
                user.is_superuser = False
                user.is_staff = False
                user.save()

    return HttpResponseRedirect(reverse('backend:users'))




@login_required
def dashboard(request):
    return render(request,
                  'editors/dashboard.html',
                  {'section': dashboard})

#Registration View
def register(request):
    args = ''
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
            args = user_form.errors
            user_form = UserRegistrationForm()
        return render(request,
                      'editors/register.html',
                      {'user_form': user_form,
                       'error': args})
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
            #Assign The Current User To the Post
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()
            messages.success(request, 'Blog Post Created Successfully')
            return HttpResponseRedirect(reverse('user_post_list'))
        else:
            messages.error(request, 'Error! Blog post was not created')
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
            cd = edit_form.cleaned_data
            title = cd['title']
            body = cd['body']
            status = cd['status']
            Post.update_post(post,title, body, status)
            #edit_form.save()
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

#Edit Magazine Newsletter Tags
@login_required
def edit_blog_post_tags(request, pk):
    #post = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = BlogEditTagsForm(request.POST or None, instance=post)
        if edit_form.is_valid():
            tags = edit_form.save(commit=False)
            edit_form.save_m2m()
            tags.save()
            messages.success(request, 'Tags updated successfully')
            return HttpResponseRedirect(reverse('user_post_list'))

        else:
            messages.error(request, 'Error updating the Tags')
            edit_form = BlogEditTagsForm(request.POST or None, instance=post)

        return render(request,
                        'editors/articles/edit-post-tags.html',
                        {'edit_form': edit_form})
    else:
        edit_form = BlogEditTagsForm(request.POST or None, instance=post)
        return render(request,
                        'editors/articles/edit-post-tags.html',
                        {'edit_form': edit_form,
                         'post': post})

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
            issue = magazine_form.save(commit=False)
            issue.author = request.user
            issue.save()
            magazine_form.save_m2m()
            #Assign The Current User To the Post
            #new_magazine.author = request.user
            #new_magazine.tags = cd['tags']
            #new_magazine.save()
            messages.success(request, 'Magazine issue was created Successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))
        else:
            messages.error(request, 'Error! Magazine issue was not created')
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
    issue = Issue.objects.get(id=pk)
    if request.method == 'POST':
        edit_form = MagazineEditForm(request.POST or None, instance=issue)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            no = cd['no']
            title = cd['title']
            description = cd['description']
            status = cd['status']
            Issue.update_issue(issue,no,title, description, status)
            messages.success(request, 'Issue updated successfully')
            return HttpResponseRedirect(reverse('user_issue_list'))

        else:
            messages.error(request, 'Error updating the Issue')
            edit_form = MagazineEditForm(request.POST or None, instance=issue)

        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form})
    else:
        edit_form = MagazineEditForm(request.POST or None, instance=issue)
        return render(request,
                        'editors/articles/issue-edit.html',
                        {'edit_form': edit_form})

#Edit Magazine Newsletter Tags
@login_required
def edit_newsletter_tags(request, pk):
    #post = get_object_or_404(Post, id=pk)
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
                        {'edit_form': edit_form})
    else:
        edit_form = MagazineEditTagsForm(request.POST or None, instance=issue)
        return render(request,
                        'editors/articles/issue-tags-edit.html',
                        {'edit_form': edit_form,
                         'issue': issue})

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
    sections = issue.sections.all().order_by('-page')
    return render(request, 'editors/articles/user_issues_sections.html',
                  {'sections': sections,
                   'issue': issue})

#Edit Newsletter Section
@login_required
def create_section(request, pk):
    issue = Issue.objects.get(id=pk)
    if request.method == 'POST':
        #Form is sent
        section_form = CreateSectionForm(data=request.POST)
        if section_form.is_valid():
            new_section = section_form.save(commit=False)
            #Assign The Current Issue To the Section
            new_section.issue = issue
            new_section.save()
            messages.success(request, 'Your Section Was added Successfully')
            return HttpResponseRedirect(reverse('user_issue_section_list',kwargs={'pk': pk}))
        else:
            messages.error(request, 'Error! Issue Section was not created')
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


# Add Section To Issue
@login_required
def add_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.added = True
    section.save()
    messages.success(request, 'Section added')
    return HttpResponseRedirect(reverse('user_issue_section_list',kwargs={'pk': issue_id}))

# Remove Section From An Issue
@login_required
def remove_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.added = False
    section.save()
    messages.success(request, 'Section was removed')
    return HttpResponseRedirect(reverse('user_issue_section_list', kwargs={'pk': issue_id}))

# Delete Section
@login_required
def delete_section(request,issue_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    messages.success(request, 'Section was deleted')
    return HttpResponseRedirect(reverse('user_issue_section_list',kwargs={'pk': issue_id}))

#Edit Edit Section
@login_required
def edit_section(request, issue_id, section_id):
    issue = Issue.objects.get(id=issue_id)
    section = Section.objects.get(id=section_id)
    section_edit_form = SectionEditForm(request.POST or None, instance=section)
    if request.method == 'POST':
        section_edit_form = SectionEditForm(request.POST or None, instance=section)
        if section_edit_form.is_valid():
            section_edit_form.save()
            messages.success(request, 'Section updated successfully')
            return HttpResponseRedirect(reverse('user_issue_section_list',kwargs={'pk': issue_id}))

        else:
            messages.error(request, 'Error updating the Section')
            section_edit_form = SectionEditForm(request.POST, instance=section)

        return render(request,
                        'editors/articles/section-edit.html',
                        {'section_edit_form': section_edit_form,
                        'issue': issue})
    else:
        return render(request,
                        'editors/articles/section-edit.html',
                        {'section_edit_form': section_edit_form,
                        'issue': issue})