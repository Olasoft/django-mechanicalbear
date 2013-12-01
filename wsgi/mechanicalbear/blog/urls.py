from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from blog.views import PostListView, PostDetailView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='list'),
    #url(r'^ajax/$', 'blog.views.ajax', name='ajax'),
    url(r'^random/$', 'blog.views.random'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post'), 
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'blog.views.doublerouble', name='monthly'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>\S+).html$', 'blog.views.doublerouble', name='slug'),
    url(r'^api/get_posts/(?P<page>\d+)/$', 'blog.views.get_posts'),
    url(r'^api/get_posts/(?P<page>\d+)/(?P<tag>\S+)/$', 'blog.views.get_posts'),
    url(r'^tag/(?P<tag>\S+)/$', PostListView.as_view(), name='list'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    #url(r'^images/(?P<path>.*.jpg)$', 'django.views.static.serve', {'document_root': 'images'}),
    #url(r'^music/(?P<path>.*.mp3)$', 'django.views.static.serve', {'document_root': 'music'}),

    url(r"^comments/", include("django.contrib.comments.urls")),
)
