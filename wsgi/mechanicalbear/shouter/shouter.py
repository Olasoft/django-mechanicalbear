#!/bin/env python
# coding: utf-8
import urllib
import json
import cgi
import os
import sys
import datetime
import pytz
import re

import sql, post_twitter, post_tumblr, post_flickr, post_facebook
from BeautifulSoup import BeautifulSoup
from secrets.vk import token

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_REPO_DIR')

if ON_OPENSHIFT:
    dryRun = False
else:
    dryRun = True

_VK_API_URL = "https://api.vk.com/method/"
wurl = _VK_API_URL + "wall.get?access_token=" + token
vurl = _VK_API_URL + "video.get?videos=%d_%d&access_token=" + token

response = urllib.urlopen(wurl)
data = response.read()
data = json.loads(data.decode("utf8")) #content_type_opts.get("charset", "utf-8")))

#print (json.dumps(data, sort_keys=True, indent=2))
act, tag_pid = sql.upsert('blog_tag', {'slug': 'pictures'}, {'name': u'картинки', })
act, tag_aid = sql.upsert('blog_tag', {'slug': 'music'},    {'name': u'саунд', })
act, tag_vid = sql.upsert('blog_tag', {'slug': 'video'},    {'name': u'видео', })
act, tag_kid = sql.upsert('blog_tag', {'slug': 'vk'},       {'name': u'вкашка', })

for entry in data['response']:
    if isinstance(entry, (int, float, complex)):
        continue
    id = entry['id']
    text = entry['text']
    date = entry['date']
    #print(date)
    #print (json.dumps(entry, sort_keys=True, indent=2))
    #print(datestr(date, 'yyyymmdd'))
    #date = datetime.datetime.fromtimestamp(date, pytz.local)
    #date = datetime.datetime.fromtimestamp(date.astimezone(pytz.utc), pytz.timezone('Asia/Yekaterinburg'))
    date = datetime.datetime.utcfromtimestamp(date)
    #date = datetime.datetime.fromtimestamp(date)
    #print(data)
    #sys.exit()
    #break

    attach_text = ""
    image = 0
    video = 0
    try:
        for attach in entry['attachments']:
            if attach['type'] == 'photo':
                #print (json.dumps(attach, sort_keys=True, indent=2))
                #sys.exit()
                pid = attach['photo']['pid']
                src = attach['photo']['src_big']
                width = attach['photo']['width']
                height= attach['photo']['height']
                ptext = attach['photo']['text']

                # downloading file
                target = 'images/' + str(pid) + '.jpg'
                if not os.path.exists(target):
                    urllib.urlretrieve(src, target)

                sql.upsert('blog_image', {'id': pid}, {'text': text, 'width': width, 'height': height})
                sql.upsert('blog_post_images', {'post_id': id, 'image_id': pid})
                sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': tag_pid})
                #text += '\n<div class=image><img src=' + src + ' /></div>'
                if image == 0:
                    image = pid

            elif attach['type'] == 'video':
                #print('video')
                #print (json.dumps(attach, sort_keys=True, indent=2))
                vid = attach['video']['vid']
                oid = attach['video']['owner_id']
                aid = attach['video']['access_key']
                title = attach['video']['title']
                descr = attach['video']['description']

                # getting link to video
                r = urllib.urlopen(vurl % (oid, vid))
                d = r.read()
                d = json.loads(d.decode("utf8"))
                #print(json.dumps(d, indent=2))
               # for e in d['response'][1]:
               #     print(json.dumps(e, indent=2))
                #print(player)
                #sys.exit()
                if d['response'][0] > 0:
                    player = d['response'][1]['player']
                    sql.upsert('blog_video', {'id': vid}, {'oid': oid, 'player': player, 'title': title, 'descr': descr})
                    sql.upsert('blog_post_videos', {'post_id': id, 'video_id': vid})
                    sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': tag_vid})
                attach_text = attach_text + " " + title
                if video == 0:
                    video = vid

            elif attach['type'] == 'audio':
                #print (json.dumps(attach, sort_keys=True, indent=2))
                #print('audio')
                aid =  attach['audio']['aid']
                url =  attach['audio']['url']
                artist = attach['audio']['artist']
                title = attach['audio']['title']
                duration = attach['audio']['duration']

                # downloading file
                target = 'music/' + str(aid) + '.mp3'
                link   = 'music/link/'
                link  += artist.replace('/', '')
                link  += ' - ' + title.replace('/', '') + '.mp3'
                if not os.path.exists(target):
                    urllib.urlretrieve(url, target)

                    i = 1
                    L = link
                    while os.path.exists(L):
                        L = link.replace('.mp3', '.' + str(i) + '.mp3')
                        i += 1
                        
                    os.symlink('../' + str(aid) + '.mp3', L)
                sql.upsert('blog_audio', {'id': aid}, {'artist': artist, 'title': title, 'duration': duration})
                sql.upsert('blog_post_audios', {'post_id': id, 'audio_id': aid})
                sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': tag_aid})
                #sys.exit()
                attach_text = attach_text + " " + artist + " - " + title + "<br />"
                    
    except KeyError:
        print ("No attachments")
    '''
    query = 
    print(query)
    print ("id: " + str(id))
    print ("text: " + text)
    '''
    p = re.compile(r'<.*?>')
    text = p.sub('', text)
    attach_text = p.sub('', attach_text)

    sql.upsert('blog_post_tags', {'post_id': id, 'tag_id': tag_kid})
    if  'insert' == sql.upsert('blog_post', {'id': id}, {'datetime': date, 'content': text, 'deleted': False}) and not dryRun:

        post_twitter.send(text, attach_text, "http://mechanicalbear.ru/" + str(id))
        post_facebook.send(id, image, video, text, attach_text)

        if image > 0:
            post_tumblr.send(id, image, date)
            post_flickr.send(id, image, text)
    #break

    sql.commit()
sql.close()
