from django import forms
from .models import BlogComment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('body',)

#Form to search for blog posts
class SearchForm(forms.Form):
    query = forms.CharField()
