from django.contrib import admin
from .models import Post, Comment, Section

# Register your models here.


class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'status', 'created')
        list_filter = ('status', )
        search_fields = ['title', 'body']


admin.site.register(Post, PostAdmin),
admin.site.register(Comment),
admin.site.register(Section)
