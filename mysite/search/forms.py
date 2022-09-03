from secrets import choice
from django import forms

#Form to search for blog posts
class SearchForm(forms.Form):
    CHOICES = (
        ('1', 'Articles'),
         ('2','Newsletters'),
         ('3', 'Device'),
    )
    choice = forms.ChoiceField(choices=CHOICES)
    query = forms.CharField()
