from django import forms
from django.contrib.auth.models import User
from blog.models import Post
from magazine.models import Issue, Section



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

class BlogEditCoverForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('cover',)

class CreateMagazineForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('no','title','description','tags','status')

class MagazineEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('no','title','description','status')

class MagazineEditCoverForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('cover',)

class MagazineEditTagsForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('tags',)

class CreateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields =('name','page','body')

class SectionEditForm(forms.ModelForm):
    class Meta:
        model = Section
        fields =('name','page','body')

