from django import forms
from .models import Feedback

#Form for sharing magazine issue
class EmailIssueForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to =  forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

#Form for Entering user feedback on magazine issue
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('body',)
