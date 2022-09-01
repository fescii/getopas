from django import forms
from .models import Review

#Form for entering user review on a particular product
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate','remarks')
