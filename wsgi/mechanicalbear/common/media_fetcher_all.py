#!/bin/env python
# coding: utf-8
import urllib
import json
import os

from secrets.vk import token

DIR = os.path.dirname(os.path.realpath(__file__))

VK_API_URL = "https://api.vk.com/method/"
wurl = VK_API_URL + "wall.get?access_token=" + token

offset = 0
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
        if isinstance(entry, (int, float, complex)): continue

        try:
            for attach in entry['attachments']:
                if attach['type'] == 'photo':
                    pid = attach['photo']['pid']
                    src = attach['photo']['src_big']

                    target = os.path.join(DIR, 'images', str(pid) + '.jpg')
                    if not os.path.exists(target):
                        r = urllib.urlretrieve(src, target)

                elif attach['type'] == 'audio':
                    continue
                    aid =  attach['audio']['aid']
                    url =  attach['audio']['url']
                    artist = attach['audio']['artist']
                    title = attach['audio']['title']
                    duration = attach['audio']['duration']

                    target = os.path.join(DIR, 'sounds', str(aid) + '.mp3')

                    link  = artist.replace('/', '')
                    link  += ' - ' + title.replace('/', '') + '.mp3'
                    link = os.path.join(DIR, 'sounds', 'link', link)

                    refetch = False
                    if os.path.exists(target):
                        local_size = os.stat(target).st_size
                        r = urllib.urlopen(url)
                        remote_size = int(r.info().getheaders('content-length')[0])
                        if local_size < remote_size:
                            print 'sound refetch', target
                            refetch = True

                    if not os.path.exists(target) or refetch:
                        r = urllib.urlretrieve(url, target)
                        print 'sound', title + ' - ' + artist

                        i = 1
                        L = link
                        while os.path.exists(L):
                            L = link.replace('.mp3', '.' + str(i) + '.mp3')
                            i += 1

                        os.symlink(target, L)
#                    else:
#                        print 'exist sound', target

                elif attach['type'] == 'video':
                    continue
                elif attach['type'] == 'link':
                    continue
                elif attach['type'] == 'album':
                    continue
                elif attach['type'] == 'doc':
                    doc = attach['doc']
                    if doc['ext'] == 'gif':
                        did = doc['did']
                        src = doc['url']

                        target = os.path.join(DIR, 'images', str(did) + '.gif')
                        if not os.path.exists(target):
                            r = urllib.urlretrieve(src, target)
                            print 'gif', target
                else:
                    print 'Attach type', attach['type']
        except KeyError as k:
            continue
        except Exception as e:
            print "Exception!", e

