# coding:utf8
from secrets.tumblr import consumer_key, consumer_secret, oauth_token, oauth_secret
import pytumblr
import sys

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    oauth_token,
    oauth_secret
)

#print client.info() #Grabs the current user information
#posts = client.posts('mechanicalbearru.tumblr.com')
#for post in posts['posts']:
#    print "#################################"
#    print " "
#    print post

#[l = client.create_link('mechanicalbearru.tumblr.com')
#print (l)
#client.create_photo("mechanicalbearru.tumblr.com", state="published" , data="/srv/http/mechanicalbear.ru/bear.jpg")

def send_link(id, text, image = "", audio = ""):
    descr = ""
    if image != "":
        descr = '<img src="http://mechanicalbear.ru/images/' + str(image) + '.jpg"><br />'
    if audio != "":
        descr += audio + '<br />'
    client.create_link('mechanicalbearru.tumblr.com',
        url="http://mechanicalbear.ru/" + str(id) + "/",
        title = text.encode("utf8"),
        description = descr.encode("utf8")
    )

#send (2767, u"жжж", 315933018, u'Кино - Закрой за мной дверь, я ухожу')

def send_image(id, image, date, text = ""):
    r = client.create_photo("mechanicalbearru.tumblr.com",
        source="http://mechanicalbear.ru/images/"+str(image)+".jpg",
        link="http://mechanicalbear.ru/"+str(id)+"/",
        caption = text,
        date = date
    )
    if r.keys()[0] == 'id':
        print('tumblr photo ' + str(image))

def send(id, image, date, text = ""):
    return send_image(id, image, date, text)
#send_image(2764, 314615686)

def send_audio(id, audio):
    r = client.create_audio("mechanicalbearru.tumblr.com",
        data="/srv/http/mechanicalbear.ru/mechanicalbear/music/"+str(audio)+".mp3",
        caption="http://mechanicalbear.ru/"+str(id)+"/"
    )
    if r.keys()[0] == 'id':
        print('tumblr audio ' + audio)

#send_audio(2761, 240349501)

def send_video(id, video):
    r = client.create_video("mechanicalbearru.tumblr.com",
        embed=video,
        caption="http://mechanicalbear.ru/"+str(id)+"/"
    )
    if r.keys()[0] == 'id':
        print('tumblr audio ' + audio)
#send_video(2676, "http://vk.com/video_ext.php?oid=404578&id=163082200&hash=e47abf0a47e69fd2403495014")

#{u'liked': False, u'followed': False, u'reblog_key': u'i3faDjKQ', u'short_url': u'http://tmblr.co/ZNRawpzpRbyH', u'id': 66361122577L, u'post_url': u'http://mechanicalbearru.tumblr.com/post/66361122577', u'can_reply': False, u'source_title': u'mechanicalbear.ru', u'image_permalink': u'http://mechanicalbearru.tumblr.com/image/66361122577', u'tags': [], u'highlighted': [], u'state': u'published', u'type': u'photo', u'format': u'html', u'timestamp': 1383907194, u'note_count': 0, u'source_url': u'http://mechanicalbear.ru', u'photos': [{u'caption': u'', u'original_size': {u'url': u'http://24.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_1280.jpg', u'width': 1000, u'height': 750}, u'alt_sizes': [{u'url': u'http://24.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_1280.jpg', u'width': 1000, u'height': 750}, {u'url': u'http://25.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_500.jpg', u'width': 500, u'height': 375}, {u'url': u'http://24.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_400.jpg', u'width': 400, u'height': 300}, {u'url': u'http://25.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_250.jpg', u'width': 250, u'height': 188}, {u'url': u'http://25.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_100.jpg', u'width': 100, u'height': 75}, {u'url': u'http://24.media.tumblr.com/289106e88dbf54df0783ed1910a8fd7c/tumblr_mvxxmi9MHC1t0fhngo1_75sq.jpg', u'width': 75, u'height': 75}]}], u'date': u'2013-11-08 10:39:54 GMT', u'slug': u'', u'blog_name': u'mechanicalbearru', u'link_url': u'http://mechanicalbear.ru/2768/', u'caption': u''}

