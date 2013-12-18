# coding: utf-8
import sqlite3
import MySQLdb
import datetime
import shutil
import os, sys

DBTYPE = 'mysql'

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    datadir = os.environ['OPENSHIFT_DATA_DIR']
    dborig  = os.path.join(datadir, 'db.sqlite3')
    dbfile  = os.path.join(datadir, 'db.sqlite3.new')
    dbhost  = os.environ['OPENSHIFT_MYSQL_DB_HOST']
    dbport  = os.environ['OPENSHIFT_MYSQL_DB_PORT']
    dbname  = os.environ['OPENSHIFT_APP_NAME']
    dbuser  = os.environ['OPENSHIFT_MYSQL_DB_USERNAME']
    dbpass  = os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
else:
    datadir = os.path.dirname(os.path.realpath(__file__))
    dborig  = os.path.join(datadir, '..', 'db.sqlite3')
    dbfile  = os.path.join(datadir, '..', 'db.sqlite3.new')
    dbhost  = 'localhost'
    dbport  = 3306
    dbname  = 'django'
    dbuser  = 'root'
    dbpass  = 'toor'

con = None
cur = None

def init(reinit = False):
    global con, cur

    if not con is None and con.open:
        if reinit: con.close
        else: return

    if DBTYPE == 'sqlite':
        shutil.copyfile(dborig, dbfile)
        con = sqlite3.connect(dbfile) #, isolation_level = 'IMMEDIATE')
    elif DBTYPE == 'mysql':
        con = MySQLdb.connect(
            host   = dbhost,
            port   = int(dbport),
            db     = dbname,
            user   = dbuser,
            passwd = dbpass,
            charset= 'utf8'
            )
    else:
        sys.exit()
    cur = con.cursor()

def v2q(v):
    if type(v) == int:
        return str(v)
    if type(v) == long:
        return str(v)
    if type(v) == datetime.datetime:
        return str(v)
    if type(v) == bool:
        return str(v)
    if v == None:
        return None

    v = v.encode("utf8").replace('\'', '\'\'')
    return v
    

def upsert(table, id, values = {}):
    w = '1 = 1'
    for k, v in id.items():
        w += ' AND `%s` = \'%s\'' % (k, str(v))

    query = u'SELECT id FROM `%s` WHERE %s' % (table, w)
    #print(query)
    cur.execute(query)

    act = 'update'
    data = cur.fetchone()
    if data is None:
        query = u'INSERT INTO `%s` ({1}) VALUES ({2})' % table
        _k = ''
        _v = ''
        for k, v in id.items():
            _k += ', `%s`' % k
            _v += ', \'%s\'' % v2q(v)
        for k, v in values.items():
            _k += ', `%s`' % k
            _v += ', \'%s\'' % v2q(v)

        query = query.replace('{1}', _k[2:])
        query = query.replace('{2}', _v[2:].decode("utf8"))
        act = 'insert'
        cur.execute(query)
        id = cur.lastrowid
    else:
        query = u'UPDATE `%s` SET {1} WHERE %s' % (table, w)
        _v = ''
        for k, v in id.items():
            _v += ', `%s` =\'%s\'' % (k, v2q(v))
        for k, v in values.items():
            #if k == 'deleted':
            if type(v) == bool:
                continue
            _v += ', `%s` =\'%s\'' % (k, v2q(v))
        query = query.replace('{1}', _v[2:].decode("utf8"))
        id = data[0]
        cur.execute(query)

    #print(query)

    return act, id

def commit():
    con.commit()

def close():
    try:
        con.close()
        if DBTYPE == 'sqlite':
            shutil.copyfile(dbfile, dborig)
            os.remove(dbfile)
    except Exception as e:
        print e

init()
