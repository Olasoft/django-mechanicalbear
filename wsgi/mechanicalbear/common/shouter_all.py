#!/bin/env python
# coding: utf-8
import urllib
import json
import os, sys
import datetime
import re

import sql
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


offset = 5
while 1:
    url = wurl + ('&offset=%d&count=100' % (offset * 100))
    offset += 1
    response = urllib.urlopen(url)
    data = response.read()
    data = json.loads(data.decode("utf8"))

    if len(data['response']) <= 1:
        break

    print '################################################################'
    print 'Next package', offset, 'length', len(data['response']), '!!!'

    for entry in data['response']:
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
        music = 0
        other = ""
        try:
            for attach in entry['attachments']:
                if attach['type'] == 'photo':
                    pid = attach['photo']['pid']
                    src = attach['photo']['src_big']
                    width = attach['photo']['width']
                    height= attach['photo']['height']
                    ptext = attach['photo']['text']

                    sql.upsert('blog_image', {'id': pid}, {'text': text, 'width': width, 'height': height, 'ext': 'jpg'})
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
                    attach_text = attach_text + " " + artist + " - " + title + "<br />"
                        
                    song = artist + ' - ' + title
                    detect_tags(tags, song)
                    if music == 0:
                        music = aid
                elif attach['type'] == 'doc':
                    did = attach['doc']['did']
                    ext = attach['doc']['ext']
                    src = attach['doc']['url']

                    if ext == 'gif':
                        sql.upsert('blog_image', {'id': did}, {'text': '', 'width': 0, 'height': 0, 'ext': ext})
                        sql.upsert('blog_post_images', {'post_id': id, 'image_id': did})

                        add_tag('gif', u'гифки')
                        tags.append('gif')

                        if image == 0:
                            image = pid
                else:
                    other = other + attach['type']

        except KeyError as k:
            continue
        except Exception as e:
            print "Exception!", e

        if music + video + image == 0:
            if len(other):
                print 'only other content', id, other, entry['text']
                continue

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
                
        #sql.commit()

sql.close()
