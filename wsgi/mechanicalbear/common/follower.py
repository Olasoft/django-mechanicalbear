#!/bin/env python
# coding: utf-8
import urllib
import json
import datetime
import os,sys
import time

from secrets.vk import token
from conf import list_followers, grouplist, text, img, myid

VK_API_URL = "https://api.vk.com/method/"
purl = VK_API_URL + "wall.post?access_token=%s" % token
purl += "&message=%s" % text
attachments = "&attachments=%s" % img
furl = VK_API_URL + "subscriptions.getFollowers?access_token=%s" % token
burl = VK_API_URL + "subscriptions.get?access_token=%s" % token
aurl = VK_API_URL + "friends.add?access_token=%s" % token
rurl = VK_API_URL + "friends.delete?access_token=%s" % token
uurl = VK_API_URL + "friends.get?access_token=%s" % token
wurl = VK_API_URL + "wall.get?access_token=%s&count=3" % token

while 1:
    try:
        #response = urllib.urlopen(wurl + '&filter=owner')
        #data = response.read()
        #data = json.loads(data.decode("utf8"))

        #attachments = '&attachments='
        #v = False
        #a = False
        #p = False
        #for item in data['response']:
        #    if isinstance(item, (int, float, complex)):
        #        continue
        #    for att in item['attachments']:
        #        if 'photo' in att and not p:
        #            attachments += "photo%d_%d," % (att['photo']['owner_id'], att['photo']['pid'])
        #            p = True
        #        if 'audio' in att and not a:
        #            attachments += "audio%d_%d," % (att['audio']['owner_id'], att['audio']['aid'])
        #            a = True
        #        if 'video' in att and not v:
        #            attachments += "video%d_%d," % (att['video']['owner_id'], att['video']['vid'])
        #            v = True

        #attachments = attachments[:-1]
        #print attachments

        #sys.exit()

        for group in grouplist:
            url = wurl + ("&owner_id=-%d" % group)
            response = urllib.urlopen(url)
            data = response.read()
            data = json.loads(data.decode("utf8"))

            post = True
            for item in data['response']:
                if isinstance(item, (int, float, complex)):
                    continue
                if item['from_id'] == myid:
                    post = False
                    break

            time.sleep(1)

            if post:
                url = purl + "&owner_id=-%d" % group + attachments
                response = urllib.urlopen(url)
                data = response.read()
                data = json.loads(data.decode("utf8"))

                print "Posting to group http://vk.com/club%d" % group, 'data',  data
            else:
                print "Post already exist on http://vk.com/club%d" % group

            time.sleep(1)

            response = urllib.urlopen(furl)
            data = response.read()
            data = json.loads(data.decode("utf8"))

            for user in data['response']['users']:
                if user not in list_followers:
                    urllib.urlopen(aurl + ("&uid=%d" % user))
                    print "Adding user:", user

            time.sleep(1)

            response = urllib.urlopen(uurl)
            data = response.read()
            data = json.loads(data.decode("utf8"))

            for user in data['response']:
                if user in list_followers:
                    urllib.urlopen(rurl + ("&uid=%d" % user))
                    print "Removing user:", user

            time.sleep(1)

            response = urllib.urlopen(burl)
            data = response.read()
            data = json.loads(data.decode("utf8"))

            for user in data['response']['users']:
                urllib.urlopen(rurl + ("&uid=%d" % user))
                print "Removing user:", user

            time.sleep(60)

    except Exception as e:
        print e
