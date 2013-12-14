from django import template
from blog.models import Tag

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
