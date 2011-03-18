from wall.models import Post, Likes
from wall.models import Comment
from django.contrib import admin

class LikesInline(admin.StackedInline):
    model = Likes
    extra = 3
    
class PostAdmin(admin.ModelAdmin):
    fields = ['publisher', 'text', 'pub_date']
    inlines = [LikesInline]
    
admin.site.register(Post, PostAdmin)