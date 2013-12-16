from django import template
from blog.models import Tag, Ads
from random import randint
import re

register = template.Library()

@register.simple_tag
def tag_menu (active_tag = None):
    tags = Tag.objects.all().filter(public = True)
    tags = tags.order_by('name')
    s = '';
    for tag in tags:
        c = ''
        if active_tag != "" and  tag.slug == active_tag.slug:
            c = " class='active' "
        s += '<a href="/tag/' + tag.slug + '"' + c + ' title="' + tag.descr + '">' + tag.name + '</a><br />\n    '
    return s

@register.simple_tag
def ads (post):
    s = ''
    if post.showAds:
        s += '<div class=ads>'
        if post.ads.count():
            ads = post.ads.all()
        else:
            ads = Ads.objects.all()

        if ads.count():
            s += '<div class=ad>'
            random_index = randint(0, ads.count() - 1)
            s += ads[random_index].content
            s += '</div>'
        s += '</div>'

    return s


@register.filter 
def hashes_to_links (value): 
    return re.sub(r"#(?!\d)(\S+)", r'<a href="/tag/\1" class=hashtag>#\1</a>', value)
