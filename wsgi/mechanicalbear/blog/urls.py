#coding: utf-8
from django.conf.urls import patterns, url

from blog.views import PostListView, PostDetailView 

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='list'), # то есть по URL http://имя_сайта/blog/ 
                                                      # будет выводиться список постов
    url(r'^random/$', PostDetailView.as_view()), # то есть по URL http://имя_сайта/blog/ 
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view()), # а по URL http://имя_сайта/blog/число/ 
                                                      # будет выводиться пост с определенным номером
)
