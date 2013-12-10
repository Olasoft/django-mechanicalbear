# coding: utf-8
import sqlite3
import datetime
import shutil
import os

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_PYTHON_IP')
if ON_OPENSHIFT:
    datadir = os.environ['OPENSHIFT_DATA_DIR']
    dborig  = os.path.join(datadir, 'db.sqlite3')
    dbfile  = os.path.join(datadir, 'db.sqlite3.new')
else:
    datadir = os.path.dirname(os.path.realpath(__file__))
    dborig  = os.path.join(datadir, '..', 'db.sqlite3')
    dbfile  = os.path.join(datadir, '..', 'db.sqlite3.new')

shutil.copyfile(dborig, dbfile)

con = sqlite3.connect(dbfile) #, isolation_level = 'IMMEDIATE')
cur = con.cursor()

def v2q(v):
    if type(v) == int:
        return str(v)
    if type(v) == datetime.datetime:
        return str(v)
    if type(v) == bool:
        return str(v)

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
            if k == 'deleted':
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
    con.close()
    shutil.copyfile(dbfile, dborig)
    os.remove(dbfile)
