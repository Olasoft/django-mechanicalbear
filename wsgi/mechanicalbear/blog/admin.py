# coding: utf-8
from django.contrib import admin
from blog.models import Post, Image, Audio, Video, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'id', 'slug', 'title', 'deleted') #, 'content')
    list_display_links = ('id', 'title')
    list_editable = ('deleted',)
    ordering = ('-datetime',)

class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration')
    list_display_links = ('artist', 'title')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'descr')
    list_display_links = ('title',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'public', 'name', 'slug')
    list_display_links = ('name',)
    list_editable = ('public',)

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)

