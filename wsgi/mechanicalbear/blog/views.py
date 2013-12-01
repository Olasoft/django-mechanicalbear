# coding: utf-8
# Create your views here.
from blog.models import Post
from django.shortcuts import redirect, render_to_response
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from random import randint
from datetime import date
from django.core import serializers
from django.forms.models import model_to_dict
import json

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        post_list = Post.objects.exclude(deleted = True).order_by('-datetime')[:10]
        return post_list

class PostDetailView(DetailView):
    model = Post

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
    #id = year + month
    year = int(year)
    month = int(month)

    #print year
    #print month
    fr = date(year, month, 1)

    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    to = date(year, month, 1)
    #print fr
    #print to
    #print slug
#    if slug == 'blog-post':
#        print str(fr) + " " + str(to) + " " + str(id)
#        blog_post = Post.objects.exclude(deleted = True).filter(datetime__range = (fr, to), id__contains = id, slug = slug).order_by('datetime')
#    else:
    print str(fr) + " " + str(to) + " " + slug
    blog_post = Post.objects.exclude(deleted = True).filter(datetime__range = (fr, to), slug = slug)

    #print blog_post

    if blog_post.count() == 0:
        print blog_post.count()
        raise Http404

    return redirect('post', blog_post[0].id)

def ajax(request):
    return render_to_response('blog/post_list_ajax.html', {})

def get_posts(request, page):
    count = 10
    fr = int(page) * count
    to = fr + count
    post_list = Post.objects.exclude(deleted = True).order_by('-datetime')[fr:to]
    jdata = serializers.serialize('json', post_list, indent=4, 
        relations = ('images', 'videos', 'audios', ))
    #print jdata
    return HttpResponse(jdata, content_type="application/json")

