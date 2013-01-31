#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *
from cm_contacts import *

import sys
print sys.getdefaultencoding()
import sqlite3
import urlparse
import urllib
import codecs

print "start"
db = sqlite3.connect('db_app.db')

#################

sql_perm_tidy = '''
SELECT app_id, perm_individual FROM permission
'''
def perms_tidy():
    print 'perm_tidy start'
    perms = {}
    apps = {}
    c = db.cursor()
    sql = 'SELECT DISTINCT(perm_individual) FROM permission'
    c.execute(sql, ())
    r = c.fetchone()
    while r != None:
        perm_original = r[0].strip()
        perm_lower = r[0].encode('utf-8').lower().strip()
        c1 = db.cursor()
        sql = 'INSERT OR IGNORE INTO perm_ids (perm_original, perm_lower) VALUES (?,?)'
        c1.execute(sql, (perm_original, perm_lower))
        db.commit()
        c1.close()
        r = c.fetchone()
    c.close()
    print 'perm_tidy ids insert'
    c = db.cursor()
    sql = 'SELECT perm_id, perm_original, perm_lower FROM perm_ids'
    c.execute(sql, ())
    r = c.fetchone()
    while r != None:
        perm_id = r[0]
        perm_original = r[1]
        perm_lower = r[2]
        if not perms.has_key(perm_lower):
            perms[perm_lower] = {}
        if not perms[perm_lower].has_key('perm_id'):
            perms[perm_lower]['perm_id'] = perm_id
        if not perms[perm_lower].has_key('perm_original'):
            perms[perm_lower]['perm_original'] = perm_original
        r = c.fetchone()
    c.close()
    print 'perm_tidy get ids'
    c = db.cursor()
    sql = 'SELECT id, app_id, perm_individual FROM permission'
    c.execute(sql, ())
    r = c.fetchone()
    while r != None:
        permission_id = r[0]
        app_id = r[1]
        perm_original = r[2].strip()
        perm_lower = r[2].encode('utf-8').lower().strip()
        perm_id = perms[perm_lower]['perm_id']
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key(perm_id):
            apps[app_id][perm_id] = {}
        apps[app_id][perm_id]['permission_id'] = permission_id
        apps[app_id][perm_id]['perm_individual'] = perm_original
        apps[app_id][perm_id]['perm_lower'] = perm_lower
        r = c.fetchone()
    c.close()
    print 'perm_tidy get permissions'
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 2)
        c1 = db.cursor()
        for perm_id in apps[app_id]:
            permission_id = apps[app_id][perm_id]['permission_id']
            perm_individual = apps[app_id][perm_id]['perm_individual']
            perm_lower = apps[app_id][perm_id]['perm_lower']
            sql = 'INSERT OR IGNORE INTO app_perm (permission_id, app_id, perm_id, perm_individual, perm_lower) VALUES (?,?,?,?,?)'
            c1.execute(sql, (permission_id, app_id, perm_id, perm_individual, perm_lower))
        db.commit()
        c1.close()
    print 'perm_tidy app_perm insert'
    print 'perm_tidy finish'


if __name__ == '__main__':
    perms_tidy()
    
