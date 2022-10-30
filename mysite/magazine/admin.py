from django.contrib import admin
from .models import Issue, Feedback

# Register your models here.
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display =  ('title','owner', 'slug', 'link', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'description','owner')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

#Registering feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('issue', 'created','active')
    list_filter = ('active', 'created', 'updated')
