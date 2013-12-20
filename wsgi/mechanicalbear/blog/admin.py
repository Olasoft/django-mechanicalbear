# coding: utf-8
from django.db import models
from django.contrib import admin
from blog.models import Post, Image, Audio, Video, Tag, Ads

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
                'deleted',
                'slug',
                'showAds',
                'ads',
                'datetime',
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
    list_display = ('id', 'ext', 'text')
    list_display_links = ('id',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'public', 'name', 'slug', 'post_count')
    list_display_links = ('name',)
    list_editable = ('public',)
    #ordering = ['post_count']

    def queryset(self, request):
        return Tag.objects.annotate(post_count = models.Count('post__tags'))

    def post_count(self, inst):
        return inst.post_count

    post_count.admin_order_field = 'post_count'
    post_count.short_description = 'Публикации'

class AdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content')
    list_display_links = ('name',)
    #list_editable = ('public',)
    ordering = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ads, AdsAdmin)

