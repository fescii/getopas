from django.contrib import admin
from .models import Issue, Feedback

# Register your models here.
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display =  ('no','title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

#Registering feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'issue', 'created','active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'description')