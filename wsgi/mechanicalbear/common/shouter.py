#!/bin/env python
# coding: utf-8
import urllib
import json
import os, sys
import datetime
import re

import sql, post_twitter, post_tumblr, post_flickr, post_facebook, post_delicious #, prostopleer
from secrets.vk import token

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_REPO_DIR')

if ON_OPENSHIFT:
    dryRun = False
else:
    dryRun = True

_VK_API_URL = "https://api.vk.com/method/"
wurl = _VK_API_URL + "wall.get?access_token=" + token
vurl = _VK_API_URL + "video.get?videos=%d_%d&access_token=" + token

all_tags = {}
def add_tag(tag, name = ''):
    global all_tags
    if not tag in all_tags:
        query = u'SELECT id FROM `blog_tag` WHERE `slug` = \'%s\'' % tag
        sql.cur.execute(query)

        data = sql.cur.fetchone()
        if data is None:
            query = u'SELECT id FROM `blog_tag` WHERE `name` = \'%s\'' % tag
            sql.cur.execute(query)
            data = sql.cur.fetchone()
            if len(name) and data is None:
                query = u'SELECT id FROM `blog_tag` WHERE `name` = \'%s\'' % name
                sql.cur.execute(query)
                data = sql.cur.fetchone()
        if data is None:
            if not len(name):
                name = tag
            query = u"INSERT INTO `blog_tag` (`slug`, `name`) VALUES ('%s', '%s')" % (tag, name)
            sql.cur.execute(query)
            tag_id = sql.cur.lastrowid
        else:
            tag_id = data[0]

        all_tags[tag] = tag_id

def detect_tag(tags, string, l, tag):
    if any(word in string.lower() for word in l):
        add_tag(tag)
        tags.append(tag)

def detect_tags(tags, string):
    detect_tag(tags, string, ['placebo', 'molko'], 'placebo')
    detect_tag(tags, string, ['nine inch nails', 'reznor'], 'nin')
    detect_tag(tags, string, ['manson'], 'mm')
    detect_tag(tags, string, [u'самойлов', u'самойлоff', 'samoiloff', u'агата кристи'], 'samoiloff')
    detect_tag(tags, string, [u'гражданская оборона', u'гроб', 'летов', u'опизденевшие'], 'letov')


response = urllib.urlopen(wurl)
data = response.read()
data = json.loads(data.decode("utf8"))

for entry in data['response'][::-1]:
    if isinstance(entry, (int, float, complex)):
        continue
    id = entry['id']
    text = entry['text']
    date = entry['date']
    tags = []

    date = datetime.datetime.utcfromtimestamp(date)

    attach_text = ""
    image = 0
    video = 0
    try:
        for attach in entry['attachments']:
            if attach['type'] == 'photo':
                pid = attach['photo']['pid']
                src = attach['photo']['src_big']
                width = attach['photo']['width']
                height= attach['photo']['height']
                ptext = attach['photo']['text']

                sql.upsert('blog_image', {'id': pid}, {'text': text, 'width': width, 'height': height})
                sql.upsert('blog_post_images', {'post_id': id, 'image_id': pid})

                #add_tag('pictures', 'картинки')
                #tags.append('pictures')

                if image == 0:
                    image = pid

            elif attach['type'] == 'video':
                vid = attach['video']['vid']
                oid = attach['video']['owner_id']
                aid = attach['video']['access_key']
                title = attach['video']['title']
                descr = attach['video']['description']

                # getting link to video
                r = urllib.urlopen(vurl % (oid, vid))
                d = r.read()
                d = json.loads(d.decode("utf8"))

                if d['response'][0] > 0:
                    player = d['response'][1]['player']
                    sql.upsert('blog_video', {'id': vid}, {'oid': oid, 'player': player, 'title': title, 'descr': descr})
                    sql.upsert('blog_post_videos', {'post_id': id, 'video_id': vid})
                    add_tag('video', 'видео')
                    tags.append('video')
                    detect_tags(tags, title)
                attach_text = attach_text + " " + title
                if video == 0:
                    video = vid

            elif attach['type'] == 'audio':
                aid =  attach['audio']['aid']
                url =  attach['audio']['url']
                artist = attach['audio']['artist']
                title = attach['audio']['title']
                duration = attach['audio']['duration']

                sql.upsert('blog_audio', {'id': aid}, {'artist': artist, 'title': title, 'duration': duration, 'link': None})
                sql.upsert('blog_post_audios', {'post_id': id, 'audio_id': aid})
                #add_tag('music', 'саунд')
                #tags.append('music')
                #sys.exit()
                attach_text = attach_text + " " + artist + " - " + title + "<br />"
                    
                song = artist + ' - ' + title
                detect_tags(tags, song)

    except KeyError:
        print ("No attachments")
    '''
    query = 
    print(query)
    print ("id: " + str(id))
    '''
    p = re.compile(r'<.*?>')
    attach_text = p.sub('', attach_text)

    t = re.sub('<[^>]*>', ' ', text)
    t = set([i[1:] for i in t.split() if i.startswith("#")])
    for tag in t:
        add_tag(tag)
        tags.append(tag)

    for tag in tags:
        if tag in all_tags:
            sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': all_tags[tag]})

    act, pid = sql.upsert('blog_post', {'id': id}, {'datetime': date, 'content': text, 'deleted': False, 'showAds': False})
            
    if  'insert' == act:
        if not dryRun:
            text = re.sub('<[^>]*>', ' ', text)
            post_twitter.send(text, attach_text, "http://mechanicalbear.ru/" + str(id))
            post_facebook.send(id, text, image, video, attach_text)
            post_delicious.send(id, text + ' ' + attach_text, tags)

            if image > 0:
                post_tumblr.send(id, image, date)
                post_flickr.send(id, image, text)
        #else:
    #break

    sql.commit()
sql.close()
