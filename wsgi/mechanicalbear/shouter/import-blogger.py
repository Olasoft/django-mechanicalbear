from secrets.blogger import username, password
import gdata
import pprint
import sql, twit
import atom

pp = pprint.PrettyPrinter(indent=4)
atom.MEMBER_STRING_ENCODING = unicode

def login(username, password):
    import gdata.service
    service = gdata.service.GDataService(username, password)
    service.service = 'blogger'
    service.server = 'www.blogger.com'
    service.ProgrammaticLogin()
    return service

def listblogs(service):
    feed = service.Get('/feeds/default/blogs')
    for blog in feed.entry:
        print "%s: %s" % (blog.GetSelfLink().href.split('/')[-1],
            blog.title.text)

def is_draft(post):
    if post.control and post.control.draft and post.control.draft.text == 'yes':
        return True
    else:
        return False

def getid(date):
    s = str(date)
    s = s.replace('-', '')
    s = s.replace('T', '')
    s = s.replace(':', '')
    return s[:12]

def listposts(service, blogid):
    feed = service.Get('/feeds/' + blogid + '/posts/default?max-results=400')
    k = 0
    for post in feed.entry:
        #print post.GetEditLink().href.split('/')[-1], post.title.text, "[DRAFT]" if is_draft(post) else ""
        #print "###############\n\n##################"
        id = getid(post.published.text)
        values = {
            'datetime':     post.published.text,
            'title':        post.title.text,
            'content':      post.content.text,
            'deleted':      is_draft(post),
            #'tags':         [],
        }
        #for tag in post.category:
        #    p['tags'].append(tag.term)
        for link in post.link:
            if link.rel == "alternate":
                values['slug'] = link.href[39:-5]
                break

        #pp.pprint (values)
        sql.upsert('blog_post', {'id': id}, values)
        #if 'insert' == sql.upsert('blog_post', {'id': id}, values):
        #    try:
        #        twit.send(post.title.text, "", "http://mechanicalbear.ru/" + str(id))
        #    except Exception as e:
        #        print (e)
        #break
        k += 1
        if k % 10 == 0:
            print k

    print k

s = login(username, password)
#listblogs(s)
listposts(s, blognumb)

sql.commit()
sql.close()
