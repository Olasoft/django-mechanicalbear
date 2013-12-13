# coding:utf8
from secrets.delicious import username, password
from pydelicious import DeliciousAPI
from getpass import getpass

api = DeliciousAPI(username, password)

def send(id, text, tags = []):
    title = ' '.join(text.split(' ')[0:4])
    tags = ', '.join(tags)
    try:
        status = api.posts_add("http://mechanicalbear.ru/" + str(id), title, extended = text, tags = tags)
    except Exception as e:
        print (e)
#    else:
#        print status

#send(3030, "Устами зануды гундосит истина!ну и мимокрокодил конечно)", ['music', 'pictures', 'vk', 'ashes'])
