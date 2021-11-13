from django.contrib import admin
from .models import Post, Profile, Comment, ForumPost, CommentForum

# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(ForumPost)
admin.site.register(CommentForum)