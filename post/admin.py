from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from . models import Post, Comment, Like, Share, Bookmark

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Like)
admin.site.register(Share)
admin.site.register(Bookmark)