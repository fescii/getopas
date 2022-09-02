from django import forms
from .models import Product, Review

#Form for entering user review on a particular product
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate','remarks')

#Create Product Form
class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'name', 'cover','model', 'series',
                  'type','company','release_date','price','about', 'tags','status')

#Edit Product Form
class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'name', 'cover','model', 'series',
                  'type','company','release_date','price','about','status')

#Edit Product Tags Form
class EditProductTags(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('tags',)