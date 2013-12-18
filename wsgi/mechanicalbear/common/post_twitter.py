from secrets.twitter import oauth_token, oauth_secret, consumer_key, consumer_secret
import twitter


auth = twitter.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
t = twitter.Twitter(auth=auth)
t.account.verify_credentials()

def send(text, snd, link):
    m = text + " " + snd
    l = 140 - len(link) - 1
    if len(m) > l:
        m = m[:l]
    m = m + " " + link
    try:
        status = t.statuses.update(status=m)
    except Exception as e:
        print (e)
    else:
        print status
