from django.contrib import admin
from .models import Tag, Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "published_date")
    list_display_links = ("title", "id")
    list_filter = ("published_date", "tags")
    search_fields = ("title", "content", "user__username")


admin.site.register(Tag)
admin.site.register(Comment)
