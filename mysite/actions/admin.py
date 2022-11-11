from django.contrib import admin
from .models import Action,UserAction

# Register your models here.
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'created']
    list_filter = ['created']
    search_fields = ['verb']

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'status', 'deleted']
    list_filter = ['created']
    search_fields = ['user']