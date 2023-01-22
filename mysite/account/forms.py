from django import forms
from django.contrib.auth.models import User
from django.forms import DateField
from .models import Profile
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

#User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.widgets.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email')
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
    date_of_birth = forms.DateField(widget=forms.DateInput)
    class Meta:
        model = Profile
        fields = ('date_of_birth','occupation','website','twitter','linkedin','location','about')
        widgets = {
            'about': SummernoteWidget(attrs={'placeholder': 'Add about'})
            #'bar': SummernoteInplaceWidget(),
        }

class ProfilePhotoEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
        labels = {"photo": "Select"}



#Moderate User Form
class ModerateUserForm(forms.Form):
    CHOICES = (
        ('1', 'admin'),
         ('2','editor'),
         ('3', 'author'),
    )
    role = forms.ChoiceField(choices=CHOICES)