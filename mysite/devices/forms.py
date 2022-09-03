from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Image, PhysicalInfo, Product, Review, SoftwareInfo

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

#Edit Physical Information Form
class CreatePhysicalInfo(forms.ModelForm):
    class Meta:
        model = PhysicalInfo
        fields = ('screen', 'battery', 'camera', 'ram', 'rom','processor','added')

#Edit Physical Information Form
class CreateSoftwareInfo(forms.ModelForm):
    class Meta:
        model = SoftwareInfo
        fields = ('os_version', 'os_name', 'os_family','os_ui','other_info','added')

#Edit Physical Information Form
class EditPhysicalInfo(forms.ModelForm):
    class Meta:
        model = PhysicalInfo
        fields = ('screen', 'battery', 'camera', 'ram', 'rom','processor','added')

#Edit Physical Information Form
class EditSoftwareInfo(forms.ModelForm):
    class Meta:
        model = SoftwareInfo
        fields = ('os_version', 'os_name', 'os_family','os_ui','other_info','added')

# Add Image Form
class AddProductPhoto(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('photo', 'added')

#Edit Image Form
class EditProductPhoto(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('photo', 'added')
