from django.contrib import admin
from .models import Post,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status',)
    list_filter = ('status','created','publish','author',)
    search_fields = ('title','body',)
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    ordering = ('status','publish',)
    date_hierarchy = 'publish'
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active',)
    list_filter = ('active','created','updated',)
    search_fields = ('name','body','email',)

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)