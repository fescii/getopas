from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm,ModerateUserForm, ProfilePhotoEditForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from actions.utils import create_action
from blog.models import Post


# Create your views here.
#verify if an user is an admin
def is_admin(user):
    return user.is_superuser and user.is_staff

# verify if an user is a moderator
def is_editor(user):
    return user.is_staff

# verify if an user is an author
def is_author(user):
    return user.is_active and not user.is_staff

#List Users
@user_passes_test(is_admin)
def list_users(request):
    user = request.user
    profile = user.profile
    user_list = User.objects.all()

    paginator = Paginator(user_list, 5) # 5 users in each page
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        users = paginator.page(paginator.num_pages)
    return render(request,
                  'account/admin/users.html',
                  {'users': users,
                   'user': user,
                   'profile': profile,
                   'section': 'users'})

# modify an user based on action
@user_passes_test(is_admin)
def moderate_user(request, user_id):
    user = request.user
    profile = user.profile
    form = ModerateUserForm(request.GET)
    u = User.objects.get(id=user_id)

    role = ''
    if u.is_superuser == True:
        role = 'admin'
    elif u.is_staff == True and u.is_superuser == False:
        role = 'editor'
    else:
        role = 'author'

    if request.method == 'POST':
        action = request.POST.get('role')
        #cd = form.cleaned_data
        #action = cd['role']

        if action == "1":
            u.is_superuser = True
            u.is_staff = True
            u.save()

        elif action == "2":
            u.is_superuser = False
            u.is_staff = True
            u.save()


        elif action == "3":
            u.is_superuser = False
            u.is_staff = False
            u.save()
        messages.success(request, 'Role updated')
        return HttpResponseRedirect(reverse('list_users'))
        """
            messages.error(request, 'Role Not Updated, Try Again!')
        """
    else:
        form = ModerateUserForm(request.GET)
        return render(request,
                          'account/admin/edit-user.html',
                          {'form': form,
                           'role': role,
                           'u': u,
                           'profile': profile,
                           'user': user})

# Removing a user based on action
@user_passes_test(is_admin)
def remove_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'User account deleted')
    return HttpResponseRedirect(reverse('list_users'))

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
            #create_action(new_user, 'has created an account')
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
        else:
            args = user_form.errors
            user_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'user_form': user_form,
                       'error': args})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'user_form': user_form})

#Edit User Info
@login_required
def edit(request,username):
    user = get_object_or_404(User,username=username)
    profile = user.profile
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return HttpResponseRedirect(reverse('profile',kwargs={'username': user.username}))

        else:
            messages.error(request, 'Error updating your profile')
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'user': user,'tab': 'profile',
                       'profile': profile,
                       'section': 'profile'})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'user': user,
                       'profile': profile,'tab': 'profile',
                       'section': 'profile'})

#User Profile Page
# @login_required
def user_profile(request, username):
    r_user = get_object_or_404(User,username=username,is_active=True)
    posts = Post.published.filter(author=r_user)
    profile = r_user.profile
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_photo_form = ProfilePhotoEditForm(data=request.POST,
                                        files=request.FILES)
            if profile_photo_form.is_valid():
                cd = profile_photo_form.cleaned_data
                photo = cd['photo']
                Profile.update_profile_picture(profile,  photo=photo)
                messages.success(request, 'Profile photo updated')
                return HttpResponseRedirect(reverse('profile',kwargs={'username': r_user.username}))

            else:
                messages.error(request, 'Error updating your profile')
                profile_photo_form = ProfilePhotoEditForm()
                return render(request,
                        'account/profile/user-profile.html',
                        {'profile_photo_form': profile_photo_form,
                        'r_user': r_user,
                        'profile': profile,'tab': 'profile',
                        'section': 'profile'})
        else:
            profile_photo_form = ProfilePhotoEditForm()
            return render(request,
                        'account/profile/user-profile.html',
                        {'r_user': r_user,
                        'profile': profile,'tab': 'profile',
                        'section': 'profile',
                        'profile_photo_form': profile_photo_form})
    else:
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
        return render(request,
                          'main/list-stories.html',
                            {'stories': posts})

    return render(request,
                 'account/profile/user-profile.html',
                    {'r_user': r_user,'stories': posts})

@login_required
def user_list(request):
    # Display all users by default
    following_ids = request.user.following.values_list('id',flat=True)
    people_only = request.GET.get('people_only')
    users = User.objects.filter(is_active=True).exclude(username=request.user.username)
    users = users.exclude(id__in=following_ids)

    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        if people_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        users = paginator.page(paginator.num_pages)
    if people_only:
        return render(request,'account/user/list-users.html',
                      {'section': 'peoples','users': users})
    return render(request,
                  'account/user/list.html',
                  {'section': 'peoples',
                   'title': 'discover',
                   'users': users})

@login_required
def top_users(request):
    # Display all users by default
    following_ids = request.user.following.values_list('id',flat=True)
    people_only = request.GET.get('people_only')
    top_ids = Post.published.order_by('-blog_views').values_list('author',flat=True)
    users = User.objects.filter(is_active=True).exclude(username=request.user.username)
    users = users.filter(id__in=top_ids)
    users = users.exclude(id__in=following_ids)
    
    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        if people_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        users = paginator.page(paginator.num_pages)
    if people_only:
        return render(request,'account/user/list-users.html',
                      {'section': 'peoples','users': users})
    return render(request,
                  'account/user/list.html',
                  {'section': 'peoples',
                   'title': 'top',
                   'users': users})

@login_required
def new_users(request):
    # Display all users by default
    following_ids = request.user.following.values_list('id',flat=True)
    people_only = request.GET.get('people_only')
    users = User.objects.filter(is_active=True).exclude(username=request.user.username)
    users = users.exclude(id__in=following_ids)
    users = users.order_by('-date_joined')

    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        if people_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        users = paginator.page(paginator.num_pages)
    if people_only:
        return render(request,'account/user/list-users.html',
                      {'section': 'peoples','users': users})
    return render(request,
                  'account/user/list.html',
                  {'section': 'peoples',
                   'title': 'new',
                   'users': users})

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'Unfollow':
                contact = Contact.objects.filter(user_from=request.user,user_to=user)
                contact.delete()
                #create_action(request.user, 'unfollowed','follow', user)
                return JsonResponse({'status':'ok'})
            elif action == 'Follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, 'is now following','follow', user)
                return JsonResponse({'status':'ok'})
            else:
                pass
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})

@login_required
def following(request,username):
    # Display all users by default
    r_user = get_object_or_404(User,username=username,is_active=True)
    following_ids = r_user.following.values_list('id',flat=True)
    users = User.objects.filter(id__in=following_ids)
    people_only = request.GET.get('people_only')

    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        if people_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        users = paginator.page(paginator.num_pages)
    if people_only:
        return render(request,'account/user/list-users.html',
                      {'section': 'peoples','users': users})
    return render(request,
                  'account/user/list.html',
                  {'section': 'peoples',
                   'title': 'following',
                   'r_user': r_user,
                   'users': users})

@login_required
def followers(request,username):
    # Display all users by default
    r_user = get_object_or_404(User,username=username,is_active=True)
    following_ids = r_user.followers.values_list('id',flat=True)
    users = User.objects.filter(id__in=following_ids)
    people_only = request.GET.get('people_only')

    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        if people_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        users = paginator.page(paginator.num_pages)
    if people_only:
        return render(request,'account/user/list-users.html',
                      {'section': 'peoples','users': users})
    return render(request,
                  'account/user/list.html',
                  {'section': 'peoples',
                   'title': 'followers',
                   'r_user': r_user,
                   'users': users})

def header_content(request):
    user = request.user
    return render(request,
                  'account/user/header.html',
                  {'section': 'people',
                   'user': user})