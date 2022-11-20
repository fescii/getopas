from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import BlogComment
from .models import *


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('body',)
        widgets = {
            'body': SummernoteWidget(attrs={'placeholder': 'Add a comment'})
            #'bar': SummernoteInplaceWidget(),
        }
       # widgets={'body': forms.Textarea(attrs={'cols': 50, 'rows': 5,'placeholder': 'Add a comment','class': 'tinymce-comment'})}

#Form to search for blog posts
class SearchForm(forms.Form):
    query = forms.CharField()
