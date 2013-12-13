# coding:utf8
from secrets.facebook import user_token
import urllib
import facebook
import sys

facebook_graph = facebook.GraphAPI(user_token)

def send(id, text, image = None, video = '', audio = ''):
    privacy = {'value': 'EVERYONE'}
    attach = {
      "link": 'http://mechanicalbear.ru/' + str(id),
      "name": text.encode("utf8"),
      #"caption": 'test',
      "description": audio.encode("utf8"),
      "privacy": privacy,
    }
    if image:
      attach["picture"] = 'http://mechanicalbear.ru/images/' + str(image) + '.jpg'

    try:
        response = facebook_graph.put_wall_post('', attachment=attach)
    except facebook.GraphAPIError as e:
        print e
    else:
        print response

