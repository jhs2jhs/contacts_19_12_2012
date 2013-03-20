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
CREATE TABLE IF NOT EXISTS perm_ids (
  perm_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  perm_original TEXT NOT NULL,
  perm_lower TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS app_perm (
  permission_id INTEGER,
  app_id TEXT NOT NULL,
  perm_id TEXT NOT NULL,
  perm_individual TEXT NOT NULL,
  perm_lower TEXT NOT NULL,
  UNIQUE (app_id, perm_id)
);
CREATE TABLE IF NOT EXISTS categories_ids (
  cate_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  cate_original TEXT NOT NULL,
  cate_lower TEXT NOT NULL UNIQUE
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
def yes_no_num(v):
    if v == None:
        return '0'
    else:
        if len(v) > 0:
            return '1'
        else:
            return '0'
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


def price_c(price):
    if price == 'install':
        price = '0'
    else:
        if not ('$' in price or '£' in price or '¥' in price):
            if price == '':
                price = '0'
            print price
        else:
            if '¥' in price:
                prices = price.split('¥')
                prices[1] = unicode(float(prices[1]) /10)
                print price, prices
            if '$' in price:
                prices = price.split('$')
                print price, prices
            if '£' in price:
                prices = price.split('£')
            price = prices[1]
    return price

def installs_c(installs):
    if '-' not in installs:
        #print installs, 0, 0
        install_min = 0
        install_max = 0
        installs = '0 - 0'
        install_average = '0'
    else:
        install = installs.split('-')
        install_min = install[0].replace(',', '').strip()
        install_max = install[1].replace(',', '').strip()
        install_average = str((int(install_min) + int(install_max))/2)
        install_min = check_none(install_min, '0')
        install_max = check_none(install_max, '0')
    return installs, install_min, install_max, install_average


########
def p_percent(p, i, i_t, percent):
    if i >= int(i_t*p/100):
        print '\t'+str(p)+'%'+'..'
        p = p + percent
    i = i + 1
    return p, i
