from django.contrib import admin
from .models import Product, PhysicalInfo, SoftwareInfo,\
    Review, Image


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author', 'release_date', 'status')
    list_filter = ('status', 'release_date', 'author')
    search_fields = ('name', 'about')
    raw_id_fields = ('author',)
    date_hierarchy = 'release_date'
    ordering = ('status',)

#Registering Physical Info Model
@admin.register(PhysicalInfo)
class PhysicalInfoAdmin(admin.ModelAdmin):
    list_display = ('screen','ram','rom','added')
    list_filter = ('added',)

#Registering SoftwareInfo Model
@admin.register(SoftwareInfo)
class SoftwareInfoAdmin(admin.ModelAdmin):
    list_display = ('os_version','os_name','added')
    list_filter = ('added',)

#Registering Reviews model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'created','active')
    list_filter = ('active', 'created', 'updated')

#Registering Image model
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'photo','cover', 'added')
    list_filter = ('added', 'cover')