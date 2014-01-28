# coding: utf-8
from blog.models import Post, Tag, Ads
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from random import randint
from datetime import date
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
import json, os
from time import sleep
import socket, re

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    host = os.environ['OPENSHIFT_PYTHON_IP']
else:
    host = '127.0.0.1'
port = 17850

def range_month(year, month):
    year = int(year)
    month = int(month)
    try:
        fr = date(year, month, 1)
    except Exception:
        return False, False

    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    to = date(year, month, 1)

    return fr, to

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        post_list = Post.objects.exclude(deleted = True)

        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            tag = get_object_or_404(Tag, Q(slug = tag) | Q(name = tag))
            post_list = post_list.filter(tags = tag)

        return post_list[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            tag = Tag.objects.get(Q(slug = tag) | Q(name = tag))
            context['tag'] = tag

        return context

class PostMonthView(ListView):
    model = Post

    def get_queryset(self):
        post_list = Post.objects.exclude(deleted = True)

        y = self.kwargs['year']
        m = self.kwargs['month']
        fr, to = range_month(y, m)
        if fr:
            post_list = post_list.filter(datetime__range = (fr, to))
        else:
            post_list = post_list[:10]

        return post_list

    def get_context_data(self, *args, **kwargs):
        context = super(PostMonthView, self).get_context_data(**kwargs)
        context['no_autoload'] = True
        return context

class PostNoTag(ListView):
    model = Post

    def get_queryset(self):
        post_list = Post.objects.exclude(deleted = True)

        post_list = post_list.filter(tags = None).order_by('-id')

        return post_list[:20]

    def get_context_data(self, *args, **kwargs):
        context = super(PostNoTag, self).get_context_data(**kwargs)
        context['no_autoload'] = True
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

def banner(request):
    ads = Ads.objects.all()
    ads = ads.filter(deleted = False, public = True)

    if ads.count():
        random_index = randint(0, ads.count() - 1)
        data = ads[random_index].content
        response = HttpResponse(data) #, content_type = "text/html")
        response["Access-Control-Allow-Origin"] = "*"
        return response

def random(request):
    blog_posts = Post.objects.exclude(deleted = True)
    count = blog_posts.count()
    if count == 0:
        raise Http404
    random_index = randint(0, count -1)

    return redirect('post', blog_posts[random_index].id)

def doublerouble(request, year, month, slug):
    year = int(year)
    month = int(month)

    fr, to = range_month(year, month)

    if fr:
        blog_post = Post.objects.exclude(deleted = True).filter(datetime__range = (fr, to), slug = slug)
    else:
        raise Http404

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
    post_list = post_list[fr:to]

    jdata = serializers.serialize('json', post_list, indent=4, 
        relations = ('images', 'videos', 'audios', 'tags', ))
    jdata = jdata.replace('\\r\\n', '\\n')
    jdata = jdata.replace('\\n', '<br />\\n')
    #print type(jdata)
    #jdata = re.sub(r"#(?!\d)(\S+)([ \"])", r"<a href='/tag/\1' class=hashtag>#\1</a>\2", jdata)
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
