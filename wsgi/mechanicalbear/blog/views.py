# coding: utf-8
from blog.models import Post, Tag
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from random import randint
from datetime import date
from django.core import serializers
from django.forms.models import model_to_dict
import json, os
from time import sleep
import socket

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    host = os.environ['OPENSHIFT_PYTHON_IP']
else:
    host = '127.0.0.1'
port = 17850

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        post_list = Post.objects.exclude(deleted = True)

        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            tag = get_object_or_404(Tag, slug = tag)
            post_list = post_list.filter(tags = tag)

        return post_list.order_by('-datetime')[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            tag = Tag.objects.get(slug = tag)
            context['tag'] = tag

        return context

class PostDetailView(DetailView):
    model = Post

    def get_object(self):
        try:
            object = super(PostDetailView, self).get_object()
        except Exception as e:
            raise Http404
        else:
            return object

def random(request):
    blog_posts = Post.objects.exclude(deleted = True)
    count = blog_posts.count()
    if count == 0:
        raise Http404
    random_index = randint(0, count -1)

    return redirect('post', blog_posts[random_index].id)

def monthly(request, year, month):
    return random(request)

def doublerouble(request, year, month, slug):
    year = int(year)
    month = int(month)

    fr = date(year, month, 1)

    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    to = date(year, month, 1)
    #print str(fr) + " " + str(to) + " " + slug
    blog_post = Post.objects.exclude(deleted = True).filter(datetime__range = (fr, to), slug = slug)

    if blog_post.count() == 0:
        #print blog_post.count()
        raise Http404

    return redirect('post', blog_post[0].id)

def get_posts(request, page, tag = None):
    count = 10
    fr = int(page) * count
    to = fr + count
    post_list = Post.objects.exclude(deleted = True)
    if not tag is None:
        post_list = post_list.filter(tags__slug = tag)
    post_list = post_list.order_by('-datetime')[fr:to]

    jdata = serializers.serialize('json', post_list, indent=4, 
        relations = ('images', 'videos', 'audios', 'tags', ))
    #print jdata
    return HttpResponse(jdata, content_type="application/json")

def content_generator():
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((host, port))
    sleeptime = 1
    while 1:
        try:
            data = r.recv(200000)
            yield data
        except Exception as e:
            print 'Disconnected '
            break
    r.close()

def radio(request):
    try:
        response = HttpResponse(content_generator(), content_type="audio/mpeg")
    except Exception as e:
        print e

    return response
