from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CreateBlogPostForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


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
    post_form = CreateBlogPostForm()
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