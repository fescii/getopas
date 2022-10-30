from django import forms
#Form to search articles, devices, and newsletters
class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Opas'}))