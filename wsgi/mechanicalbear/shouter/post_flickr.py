# coding:utf8
from secrets.flickr import api_key, api_secret, final_oauth_token, final_oauth_token_secret
from flickr import FlickrAPI

f = FlickrAPI(api_key=api_key,
    api_secret=api_secret,
    oauth_token=final_oauth_token,
    oauth_token_secret=final_oauth_token_secret)

#recent_activity = f.get('flickr.activity.userComments')
#print recent_activity

def send(id, photo, text):
    data=u"images/"+unicode(str(photo))+u".jpg"
    if not len(text):
        text = str(id)
    params = {
        'title': text,
        'description': u'Источник <a href="http://mechanicalbear.ru/%s">mechanicalbear.ru/%s</a>' % (id, id),
        'tags': 'mechanicalbear.ru регби любовь рокнролл',
    }
    add_photo = {}
    try:
        with open(data, u'r') as files:
            add_photo = f.post( params = params, files = files )
    except Exception as e:
        print data
        print params
        print e
    else:
        print add_photo


