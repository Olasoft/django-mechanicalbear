#!/bin/env python
# coding: utf-8
import urllib
import json
import os

from secrets.vk import token

DIR = os.path.dirname(os.path.realpath(__file__))

VK_API_URL = "https://api.vk.com/method/"
wurl = VK_API_URL + "wall.get?access_token=" + token

response = urllib.urlopen(wurl)
data = response.read()
data = json.loads(data.decode("utf8"))

for entry in data['response'][::-1]:
    if isinstance(entry, (int, float, complex)): continue

    try:
        for attach in entry['attachments']:
            if attach['type'] == 'photo':
                pid = attach['photo']['pid']
                src = attach['photo']['src_big']

                target = os.path.join(DIR, 'images', str(pid) + '.jpg')
                if not os.path.exists(target):
                    urllib.urlretrieve(src, target)

            elif attach['type'] == 'audio':
                aid =  attach['audio']['aid']
                url =  attach['audio']['url']
                artist = attach['audio']['artist']
                title = attach['audio']['title']
                duration = attach['audio']['duration']

                target = os.path.join(DIR, 'sounds', str(aid) + '.mp3')

                link  = artist.replace('/', '')
                link  += ' - ' + title.replace('/', '') + '.mp3'
                link = os.path.join(DIR, 'sounds', 'link', link)

                if not os.path.exists(target):
                    urllib.urlretrieve(url, target)

                    i = 1
                    L = link
                    while os.path.exists(L):
                        L = link.replace('.mp3', '.' + str(i) + '.mp3')
                        i += 1
                        
                    os.symlink(target, L)
            elif attach['type'] == 'doc':
                doc = attach['doc']
                if doc['ext'] == 'gif':
                    did = doc['did']
                    src = doc['url']

                    target = os.path.join(DIR, 'images', str(did) + '.gif')
                    if not os.path.exists(target):
                        r = urllib.urlretrieve(src, target)
                        print 'gif', target
    except KeyError:
        print ("No attachments")

