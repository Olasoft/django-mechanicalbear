#!/bin/env python
# coding:utf8
from threading import Thread as t
import threading 
from time import sleep
from mutagen.mp3 import MP3 as mp3
from mutagen.easyid3 import EasyID3
import socket, os, sys
import urllib

sleeptime = 1

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    host = os.environ['OPENSHIFT_PYTHON_IP']
    datadir = os.environ['OPENSHIFT_DATA_DIR'] 
    datadir = os.path.join(datadir, 'streamer')
else:
    host = '127.0.0.1'
    datadir = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.join(datadir, '../../static/music/')
main_port = 5555

playlist = os.path.join(datadir, u'list.txt')

qusers = 0
ports = []

main_stream = "socket_"
tmp_sock = "/tmp/stream.socket"
header  = 'HTTP/1.0 200 OK\r\n'
header += 'Content-Type: audio/mpeg\r\n'
header += '\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

p = open(playlist)
plist = []
for line in p:
    line = os.path.join(datadir, line.replace('\n', ''))
    if line == '': continue
    audiofile = {
        'path': line
    }

    minfo = mp3(audiofile['path'], ID3=EasyID3)
    stat = os.stat(audiofile['path'])
    bufsize = stat.st_size / minfo.info.length
    bufsize = int(bufsize * sleeptime) + 100
    audiofile['bitrate'] = minfo.info.bitrate
    audiofile['bufsize'] = bufsize
    #print audiofile['bufsize']
    #bufsize = int(minfo.info.bitrate / (8 / sleeptime))
    #print bufsize
    #sys.exit()
    audiofile['name'] = audiofile['path']

    if 'artist' in minfo:
        audiofile['artist'] = minfo['artist'][0]
        audiofile['name']   = minfo['artist'][0]
    if 'title' in minfo:
        audiofile['title']  = minfo['title'][0]
        audiofile['name']  += ' - ' + minfo['title'][0]

    plist.append(audiofile)

def datasender(conn, addr):
    global qusers
    qusers += 1
    port = main_port + qusers
    #port = main_stream + str(qusers)
    #try:
    #    os.remove(port)
    #except OSError:
    #    pass
    ports.append(port)
    #r = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #r.bind(port)
    r.bind((host, port))
    print 'Connected by %s %d (%d)' % (addr[0], port, len(ports))
    #print 'Connected by %s %s (%d)' % (addr[0], port, len(ports))
    #print ports
    #conn.sendall(header)
    while 1:
        data = r.recv(200000)
        if not data: 
            print 'End sending data', addr
            sleep(sleeptime)
        try:
            conn.sendall(data)
        except Exception as e:
            print 'Disconnected ', addr
            conn.close()
            break
    conn.close()
    #try:
    #    os.remove(port)
    #except OSError:
    #    pass
    ports.remove(port)


def listen():
    w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #print lock.locked()
        w.bind((host, main_port))
        #lock.acquire()
    except Exception as e:
        print e
        return
    #try:
    #    os.remove(tmp_sock)
    #except OSError:
    #    pass
    #w.bind(tmp_sock)

    w.listen(1)
    print 'Server listening'
    while 1:
        conn, addr = w.accept()
        sender = t(target = datasender, args = (conn, addr))
        sender.start()
    #lock.release()

def stream():
    #s.bind(main_stream)
    while 1:
        print 'start playlist'
        for track in plist:
            #print track['name'], track['bufsize']
            r = open(track['path'])
            #r.seek(6000000)
            buf = r.read(track['bufsize'])
            
            i = 0
            while buf != '':
                #s.flush()
                #print i
                for port in ports:
                    #s.sendto(buf, port)
                    s.sendto(buf, (host, port))
                #print 'sendto'

                buf = r.read(track['bufsize'])
                i += 1

                sleep(sleeptime)
            r.close()
            sleep(sleeptime)
        print 'end playlist'

#@get('/stream.mp3')
#def web():
#    stream = urllib.urlopen('http://'+host+':'+str(main_port)+'/')
#    response.content_type = 'audio/mpeg'
#    return stream.read()

#if __name__ == "__main__":
listener = t(target = listen, args = ())
streamer = t(target = stream, args = ())

listener.start()
streamer.start()
#listen()

#run(host='127.0.0.1', port = 5000, reloader=False) #, debug=True)

#listener.join()
#streamer.join()
