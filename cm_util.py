#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#sys.setdefaultencoding('iso-8859-1')
print sys.getdefaultencoding()

#### encoding: utf-8 

import sqlite3
import urlparse
import urllib
import codecs

print "start"
db = sqlite3.connect('db_app.db')

sql_init = '''
CREATE TABLE IF NOT EXISTS app_contact (
  app_id TEXT NOT NULL UNIQUE,
  perm TEXT -- cr, cw, pr, pw, sr, sw
);
'''

c = db.cursor()
c.executescript(sql_init)
db.commit()
c.execute('SELECT * FROM SQLITE_MASTER')
tables = c.fetchall()
print '** tables: %s **'%(str(len(tables)))
c.close()


#############
def get_url_query(urls, key):
    urls_qs = urlparse.urlparse(urls).query
    urls_q = urlparse.parse_qs(urls_qs)
    if urls_q.has_key(key) and len(urls_q[key]) > 0:
        urls = urls_q[key][0]
    urls = urls.lower().strip()
    return urls
def check_none(v, empty):
    if v == '':
        return empty
    if type(v) == unicode:
        v = v.encode('utf-8', 'replace')
    else:
        v = str(v)
        v = unicode(v, 'utf-8')
    v = v.strip()
    return v
def figures(google_plus_figure, k, t):
    if k in google_plus_figure:
        google_plus_figures = google_plus_figure.split(k)
        google_plus_figure = google_plus_figures[0]
        google_plus_figure = float(google_plus_figure.replace(',', ''))
        google_plus_figure = google_plus_figure * t
        google_plus_figure = unicode(google_plus_figure)
    if type(google_plus_figure) == unicode:
        google_plus_figure = google_plus_figure.encode('utf-8', 'replace')
    else:
        google_plus_figure = str(google_plus_figure)
    return google_plus_figure
def yes_no(v):
    if v == '':
        return '0'
    else:
        if v == 'none':
            return '0'
        else:
            return '1'
def contact_level(perms):
    s = 0
    i = 0
    if 'c' in perms and not 'p' in perms and not 's' in perms:
        s = 1
        i = 1
    if 'c' in perms and 'p' in perms and not 's' in perms:
        s = 2
        i = 1
    if 'c' in perms and not 'p' in perms and 's' in perms:
        s = 3
        i = 1
    if 'c' in perms and 'p' in perms and 's' in perms:
        s = 4
        i = 1
    s = unicode(s)
    i = unicode(i)
    return s, i
                    
#############

def d_zero(m, n):
    if n == 0:
        return 0
    k = m*1.0/n
    return k
