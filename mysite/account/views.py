from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm,ModerateUserForm, ProfilePhotoEditForm

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
                  'editors/admin/users.html',
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
        messages.success(request, 'Role updated successfully')
        return HttpResponseRedirect(reverse('list_users'))
        """
            messages.error(request, 'Role Not Updated, Try Again!')
        """
    else:
        form = ModerateUserForm(request.GET)
        return render(request,
                          'editors/admin/edit-user.html',
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
    messages.success(request, 'User account was successfully deleted')
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
    user = request.user
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
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(reverse('profile',kwargs={'username': user.username}))

        else:
            messages.error(request, 'Error updating your profile')
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            return render(request,
                      'editors/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'user': user,
                       'profile': profile})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'editors/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'user': user,
                       'profile': profile})

#User Profile Page
@login_required
def user_profile(request, username):
    r_user = User.objects.get(username=username)
    profile = r_user.profile
    if request.method == 'POST':
        profile_photo_form = ProfilePhotoEditForm(data=request.POST,
                                       files=request.FILES)
        if profile_photo_form.is_valid():
            cd = profile_photo_form.cleaned_data
            photo = cd['photo']
            Profile.update_profile_picture(profile,  photo=photo)
            messages.success(request, 'Profile photo updated successfully')
            return HttpResponseRedirect(reverse('profile',kwargs={'username': r_user.username}))

        else:
            messages.error(request, 'Error updating your profile')
            profile_photo_form = ProfilePhotoEditForm()
            return render(request,
                      'editors/edit.html',
                      {'profile_photo_form': profile_photo_form,
                       'r_user': r_user,
                       'profile': profile,
                       'section': 'profile'})

    else:
        profile_photo_form = ProfilePhotoEditForm()
        return render(request,
                    'account/profile/user-profile.html',
                    {'r_user': r_user,
                    'profile': profile,
                    'section': 'profile',
                    'profile_photo_form': profile_photo_form})
