#/bin/env python
# coding:utf8
from secrets.prostopleer import oauth_id, oauth_token
import urllib, urllib2, base64, json

main_token = ''

def get_token(oauth_id, oauth_token):
    auth = 'http://api.pleer.com/token.php'

    request = urllib2.Request(auth)
    base64string = base64.encodestring('%s:%s' % (oauth_id, oauth_token)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    data = {
        'grant_type': 'client_credentials',
    }
    result = urllib2.urlopen(request, urllib.urlencode(data))

    access = result.read()

    access = json.loads(access)

    main_token = access['access_token']

    return main_token

def search_track(query):
    global main_token
    url = 'http://api.pleer.com/index.php'
    data = {
        'access_token': main_token,
        'method': 'tracks_search',
        'query': query,
    }
    data = urllib.urlencode(dict([k.encode('utf-8'),unicode(v).encode('utf-8')] for k,v in data.items()))
    result = urllib2.urlopen(url, data)
    r = result.read()
    r = json.loads(r)
    if r['success']:
        return r['tracks']
    else:
        return False
    
def get_link(id):
    global main_token
    url = 'http://api.pleer.com/index.php'
    data = {
        'access_token': main_token,
        'method': 'tracks_get_download_link',
        'track_id': id,
        'reason': 'listen',
    }
    result = urllib2.urlopen(url, urllib.urlencode(data))
    r = result.read()
    r = json.loads(r)
    if r['success']:
        return r['url']
    else:
        return False

def get_track_url(artist, title, lenght = 0):
    if len(artist):
        query = artist
        query += ' '
    if len(title):
        query += title
    if not len(query):
        return None

    print query

    plist = search_track(query)
    if not len(plist):
        return False
    t = plist.items()[0]
    for id, track in plist.items():
        if lenght:
            if track['lenght'] == lenght:
                t = track
                break
        else:
            t = track
            break
    link = get_link(track['id'])
    return link

main_token = get_token(oauth_id, oauth_token)

#url = get_track_url('Жанна Агузарова', 'Hasta siempre Comandante', 193)
