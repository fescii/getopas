from django import forms

class EmailIssueForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to =  forms.EmailField()
    comments = forms.forms.CharField(required=False,
                                     Widget=forms.Textarea)