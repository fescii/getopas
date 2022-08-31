from django import forms
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post
from magazine.models import Issue, Section
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
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

#User Details Edit Form
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth','about','photo')


#Moderate User Form
class ModerateUserForm(forms.Form):
    user_types = (('admin','editor','normal'),)
    role = forms.ChoiceField(choices=user_types)

#User/Editor Creating a Blog Post
class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','tags','status')
class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body','status')
        #fields = '__all__'

class BlogEditTagsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('tags',)

class CreateMagazineForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('no','title','description','tags','status')

class MagazineEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('no','title','description','status')
class MagazineEditTagsForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('tags',)

class CreateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields =('name','page','body','added')

class SectionEditForm(forms.ModelForm):
    class Meta:
        model = Section
        fields =('name','page','body','added')
