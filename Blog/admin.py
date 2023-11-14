from django.contrib import admin
from .models import (
    Post,
    PostTags,
    PostComment,
    PostRate,
)


class PostCommentInline(admin.TabularInline):
    model = PostComment


class PostTagsInline(admin.TabularInline):
    model = PostTags


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "Title",
        "Demo",
        "Created",
        "Modified_At",
        "Active",
    ]
    inlines = [PostCommentInline, PostTagsInline]
    search_fields = ("Title", "")
    ordering = ("Created_At", "Modified_At", "Rate")
