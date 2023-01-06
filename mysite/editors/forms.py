from django import forms
from django.contrib.auth.models import User
from blog.models import Post
from magazine.models import Issue
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



#User/Editor Creating a Blog Post
class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','tags','status')
        widgets = {
            'body': SummernoteWidget(),
            # 'title': {'placeholder': 'Search Opas','is_required':'required'},
        }
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
        fields = ('title','owner','release','description','platform','tags','status','link')

class MagazineEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title','owner','release','description','platform','status','link')

class MagazineEditCoverForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('cover',)

class MagazineEditTagsForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('tags',)


