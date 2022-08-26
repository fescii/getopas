from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm,\
    UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


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
        else:
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