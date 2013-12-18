#!/bin/env python
# coding:utf8
from threading import Thread as t
import threading 
from time import sleep
from mutagen.mp3 import MP3 as mp3
from mutagen.easyid3 import EasyID3
import socket, os, sys
import urllib
import sql

sleeptime = 1
radiolimit = 30

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    host = os.environ['OPENSHIFT_PYTHON_IP']
    datadir = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'music')
else:
    host = '127.0.0.1'
    datadir = 'http://149.154.69.37/sounds/'
main_port = 17850

qusers = 0
ports = []

main_stream = "socket_"
tmp_sock = "/tmp/stream.socket"
header  = 'HTTP/1.0 200 OK\r\n'
header += 'Content-Type: audio/mpeg\r\n'
header += '\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def datasender(conn, addr):
    global qusers
    qusers += 1
    port = main_port + qusers
    ports.append(port)
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r.bind((host, port))
    print 'Connected by %s %d (%d)' % (addr[0], port, len(ports))
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
    ports.remove(port)

def listen():
    w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        w.bind((host, main_port))
    except Exception as e:
        print e
        sys.exit()
        return

    w.listen(1)
    print 'Server listening on', str(main_port)
    while 1:
        conn, addr = w.accept()
        sender = t(target = datasender, args = (conn, addr))
        sender.start()

def stream():
    current_track = None

    while 1:
        query = u'''
            select
                id,
                artist,
                title,
                duration
            from blog_audio
            where radio = 1
            order by id desc
            limit %d
        ''' % radiolimit

        sql.cur.execute(query)
        plist = sql.cur.fetchall()
        sql.cur.close()
        sql.con.close()

        id = 0
        for track in plist:
            if current_track is None or track[0] < current_track[0]:
                current_track = track
                break
            id += 1
        if id >= radiolimit:
            current_track = plist[0]

        path = os.path.join(datadir, str(current_track[0]) + '.mp3')
        name = '%s - %s' % (current_track[1], current_track[2])

        if path[:7] == 'http://':
            r = urllib.urlopen(path)
            meta = r.info()
            bufsize = meta.getheaders("Content-Length")[0]
            bufsize = int(bufsize)
        else:
            r = open(path)
            stat = os.stat(path)
            bufsize = stat.st_size

        bufsize = bufsize / track[3]
        bufsize = int(bufsize * sleeptime) + 100

        buf = r.read(bufsize)
        
        while buf != '':
            for port in ports:
                s.sendto(buf, (host, port))
            buf = r.read(bufsize)
            sleep(sleeptime)

        r.close()
        sleep(sleeptime)

listener = t(target = listen, args = ())
streamer = t(target = stream, args = ())

listener.start()
streamer.start()

listener.join()
streamer.join()
