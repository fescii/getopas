from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post
#User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.widgets.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    def clean_password2(self):
        cd =  self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match!')
        return cd['password2']

#User Details Edit Form
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth','about','photo')

#User/Editor Creating a Blog Post
class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','tags','status')
class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body','tags','status')
