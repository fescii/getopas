from django.contrib import admin

# Register your models here.
from .models import Post, BlogComment,Bookmark
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('post', 'added', 'user')
    list_filter = ('added',)
