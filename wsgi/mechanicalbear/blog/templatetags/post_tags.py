from django import template
from blog.models import Tag

register = template.Library()

@register.simple_tag
def tag_menu ():
    tags = Tag.objects.all().filter(public = True)
    s = '';
    for tag in tags:
        s += '<a href="/tag/' + tag.get_url() + '">' + tag.name + '</a><br />'
    return s
