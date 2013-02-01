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
def perms_tidy_ids_insert():
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

def perms_tidy_permissions():
    apps = {}
    perms = {}
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
        pi = p
        p, i_i = p_percent(p, i_i, i_t, 10)
        c1 = db.cursor()
        for perm_id in apps[app_id]:
            permission_id = apps[app_id][perm_id]['permission_id']
            perm_individual = apps[app_id][perm_id]['perm_individual']
            perm_lower = apps[app_id][perm_id]['perm_lower']
            sql = 'INSERT OR IGNORE INTO app_perm (permission_id, app_id, perm_id, perm_individual, perm_lower) VALUES (?,?,?,?,?)'
            c1.execute(sql, (permission_id, app_id, perm_id, perm_individual, perm_lower))
        if pi < p:
            db.commit()
        c1.close()
    db.commit()
    print 'perm_tidy app_perm insert'
    print 'perm_tidy finish'

def perms_get(perms):
    print 'perms_get start'
    sql = 'SELECT perm_id, perm_lower FROM perm_ids'
    c = db.cursor()
    c.execute(sql, ())
    r = c.fetchone()
    while r != None:
        perm_id = r[0]
        perm_lower = r[1]
        if not perms.has_key(perm_id):
            perms[perm_id] = perm_lower
        r = c.fetchone()
    c.close()
    print 'perms_get end'
    return perms

def perms_fact_perms_print(perms):
    print 'perm_fact_perms_print start'
    f = codecs.open('./txt/cm_perm_fact_perms.txt', 'w', encoding='utf-8')
    f.write('perm_id\tperm_lable\n')
    for perm_id in perms:
        perm_lower = perms[perm_id]
        t = u'%s\t%s\t\n'%(perm_id, perm_lower)
        f.write(t)
    f.close()
    print 'perms_fact_perms_print end'

#######
def categories_tidy():
    print 'categories_tidy start'
    categories = {}
    c = db.cursor()
    sql = 'SELECT category FROM app WHERE developer_href IS NOT NULL and category IS NOT NULL'
    c.execute(sql, ())
    r = c.fetchone()
    print 'before loop'
    i = 0
    while r != None:
        cate_original = r[0]
        if cate_original == None:
            r = c.fetchone()
            continue
        if cate_original.strip() == '':
            r = c.fetchone()
            continue
        if categories.has_key(cate_original):
            r = c.fetchone()
            #print cate_original
            continue
        categories[cate_original] = True
        #i = i + 1
        #if i % 10000 == 0:
        #    print i % 1000, i, categories
        #print cate_original
        cate_lower = r[0].encode('utf-8').lower().strip()
        c1 = db.cursor()
        sql = 'INSERT OR IGNORE INTO categories_ids (cate_original, cate_lower) VALUES (?,?)'
        c1.execute(sql, (cate_original, cate_lower))
        db.commit()
        c1.close()
        r = c.fetchone()
    c.close()
    print 'categories_tidy ids insert'

def category_get(categories):
    print 'category_get start'
    sql = 'SELECT cate_id, cate_lower FROM categories_ids'
    c = db.cursor()
    c.execute(sql, ())
    r = c.fetchone()
    while r != None:
        cate_id = r[0]
        cate_lower = r[1]
        if not categories.has_key(cate_id):
            categories[cate_lower] = cate_id
        r = c.fetchone()
    c.close()
    print 'category_get end'
    return categories

def perms_fact_categories_print(categories):
    print 'perm_fact_categories_print start'
    f = codecs.open('./txt/cm_perm_fact_categories.txt', 'w', encoding='utf-8')
    f.write('cate_id\tcate_lable\n')
    for cate_lower in categories:
        cate_id = categories[cate_lower]
        t = u'%s\t%s\t\n'%(cate_id, cate_lower)
        f.write(t)
    f.close()
    print 'perms_fact_categories_print end'


if __name__ == '__main__':
    categories_tidy()
    categories = {}
    categories = category_get(categories)
    perms_fact_categories_print(categories)
    ##
    perms_tidy_ids_insert()
    perms = {}
    perms = perms_get(perms)
    perms_fact_perms_print(perms)
    ##
    perms_tidy_permissions()
   
    
    
