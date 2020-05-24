from django.contrib import admin
from .models import BlogType, Blog
from read_statistics.models import ReadNum

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

  

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'created_time', 'last_updated_time','get_read_num')

# @admin.register(ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')