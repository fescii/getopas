from django import forms

#Form to search articles, devices, and newsletters
class SearchForm(forms.Form):
    CHOICES = (
        ('one', 'Articles'),
         ('two','Newsletters'),
         ('three', 'Device'),
    )
    option = forms.ChoiceField(choices=CHOICES)
    query = forms.CharField()
