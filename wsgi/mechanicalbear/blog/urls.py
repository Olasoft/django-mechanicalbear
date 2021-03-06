from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from blog.views import PostListView, PostDetailView, PostNoTag, PostMonthView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^radio.mp3$', 'blog.views.radio', name='radio'),
    url(r'^random/$', 'blog.views.random'),
    url(r'^banner/$', 'blog.views.banner'),
    url(r'^notag/$', PostNoTag.as_view(), name='notag'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post'), 
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', PostMonthView.as_view(), name='monthly'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>\S+).html$', 'blog.views.doublerouble', name='slug'),
    url(r'^api/get_posts/(?P<page>\d+)/$', 'blog.views.get_posts'),
    url(r'^api/get_posts/(?P<page>\d+)/(?P<tag>\S+)/$', 'blog.views.get_posts'),
    url(r'^tag/(?P<tag>\S+)/$', PostListView.as_view(), name='list'),
    url(r'^search/label/(?P<tag>\S+)/$', PostListView.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    #url(r'^images/(?P<path>.*.jpg)$', 'django.views.static.serve', {'document_root': 'images'}),
    #url(r'^music/(?P<path>.*.mp3)$', 'django.views.static.serve', {'document_root': 'music'}),

    url(r"^comments/", include("django.contrib.comments.urls")),
)
