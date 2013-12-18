#!/bin/env python
# coding: utf-8
from secrets.blogger import username, password, blognumb
import gdata
import pprint
import sql
import atom
from sys import exit
from transliterate.utils import translit

pp = pprint.PrettyPrinter(indent=4)
atom.MEMBER_STRING_ENCODING = unicode

def login(username, password):
    import gdata.service
    service = gdata.service.GDataService(username, password)
    service.service = 'blogger'
    service.server = 'www.blogger.com'
    service.ProgrammaticLogin()
    return service

def listblogs(service):
    feed = service.Get('/feeds/default/blogs')
    for blog in feed.entry:
        print "%s: %s" % (blog.GetSelfLink().href.split('/')[-1],
            blog.title.text)

def is_draft(post):
    if post.control and post.control.draft and post.control.draft.text == 'yes':
        return True
    else:
        return False

def getid(date):
    s = str(date)
    s = s.replace('-', '')
    s = s.replace('T', '')
    s = s.replace(':', '')
    return s[:12]

def listposts(service, blogid):
    feed = service.Get('/feeds/' + blogid + '/posts/default?max-results=400')
    k = 0
    all_tags = {}
    for post in feed.entry:
        #print post.GetEditLink().href.split('/')[-1], post.title.text, "[DRAFT]" if is_draft(post) else ""
        #print "###############\n\n##################"
        id = getid(post.published.text)
        values = {
            'datetime':     post.published.text,
            'title':        post.title.text,
            'content':      post.content.text,
            'deleted':      is_draft(post),
        }
        tags = []
        for tag in post.category:
            if not tag.term in all_tags:
                slug = translit(tag.term, "ru", reversed=True)
                slug = slug.replace(' ', '_')
                slug = slug.replace('-', '_')
                slug = slug.replace('.', '')
                slug = slug.replace(',', '')
                slug = slug.replace('\'', '')
                slug = slug.replace('\"', '')
                new_tag = {
                    'slug': slug,
                    'name': tag.term,
                }
                act, tid = sql.upsert('blog_tag', {'slug': slug}, {'name': tag.term, })
                new_tag['id'] = tid

                all_tags[tag.term] = new_tag

            tags.append(all_tags[tag.term]['id'])

        for link in post.link:
            if link.rel == "alternate":
                values['slug'] = link.href[39:-5]
                break

        #pp.pprint (all_tags)
        #pp.pprint (tags)
        for tid in tags:
            sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': tid})

        #sql.upsert('blog_post', {'id': id}, values)
        #if 'insert' == sql.upsert('blog_post', {'id': id}, values):
        #    try:
        #        twit.send(post.title.text, "", "http://mechanicalbear.ru/" + str(id))
        #    except Exception as e:
        #        print (e)
        #break
        k += 1
        if k % 10 == 0:
            print k

    print k

s = login(username, password)
#listblogs(s)
listposts(s, blognumb)

sql.commit()
sql.close()
