from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'due_datetime', 'priority', 'repeat', 'is_done']
    list_filter = ['priority', 'repeat', 'is_done']
    search_fields = ['title', 'user__username']
