# coding: utf-8
from django.contrib import admin
from blog.models import Post, Image, Audio, Video, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'id', 'slug', 'title', 'deleted') #, 'content')
    list_display_links = ('id', 'title')
    list_editable = ('deleted',)
    ordering = ('-datetime',)
    list_filter = ('tags', )
    filter_horizontal = ('tags',)
    #list_select_related = False
    #filter_vertical = ('images',)
    #raw_id_fields = ('images',)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'content',
                'tags',
                ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Дополнительно', {
            'fields': (
                'datetime',
                'slug',
                'deleted',
            ),
            'classes': ('collapse', 'wide', 'extrapretty'),
        }),
        ('Вложения', {
            'fields': (
                'audios',
                'images',
                'videos',
            ),
            'classes': ('collapse', 'wide', 'extrapretty'),
        }),
    )

class AudioAdmin(admin.ModelAdmin):
    list_display = ('radio', 'title', 'artist', 'get_duration')
    list_display_links = ('artist', 'title')
    list_editable = ('radio',)
    ordering = ('-id',)

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
    ordering = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)

