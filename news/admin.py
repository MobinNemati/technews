from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'counted_view', 'status', 'published_date', 'updated_date', 'created_date')
    list_filter = ('status', 'author')
    #ordering = ['created_date',]
    search_fields = ['title', 'content']
    summernote_fields = ('content',)



class CommentAdmin(ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name', 'post', 'approved', 'created_date')
    list_filter = ('post', 'approved')
    search_fields = ['name', 'post']



class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)