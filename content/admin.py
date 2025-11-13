from unfold.admin import ModelAdmin
from django.contrib import admin
from content.models import Blog, Comment, Tag


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['id', 'body']


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['id', 'name']
