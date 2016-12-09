from django.contrib import admin
from .models import Bookmark,Link
from django.contrib.auth.models import User

class BookmarkItem(admin.ModelAdmin):
    list_display = ['title','link']

class LinkItem(admin.ModelAdmin):
    list_display = ['url']

admin.site.register(Bookmark, BookmarkItem)
admin.site.register(Link,LinkItem)

