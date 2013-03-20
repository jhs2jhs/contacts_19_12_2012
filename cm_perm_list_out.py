#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *
from cm_contacts import *
from cm_perm_tidy import *

import sys
print sys.getdefaultencoding()
import sqlite3
import urlparse
import urllib
import codecs
import cm_contacts

print "start"
db = sqlite3.connect('db_app.db')

#################

sql_perm_fact_perms = '''
SELECT app_id, perm_id, perm_individual, perm_lower FROM app_perm
'''
def perms_get(perm_list):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        if not perm_list.has_key(perm_id):
            perm_list[perm_id] = {}
            perm_list[perm_id]['app_id'] = app_id
            perm_list[perm_id]['perm_lower'] = perm_lower
            print len(perm_list), perm_id, perm_lower, app_id
        if len(perm_list) == 230:
            break
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    #print apps
    return perm_list

    
def perms_get_print(perm_list):
    f = codecs.open('./txt/cm_perm_list_out.txt', 'w', encoding='utf-8')
    t = u'perm_id\tperm_lower\tapp_id\n'
    f.write(t)
    for perm_id in perm_list:
        perm_lower = perm_list[perm_id]['perm_lower']
        app_id = perm_list[perm_id]['app_id']
        t = u'%s\t%s\t%s\t\n'%(perm_id, perm_lower, app_id)
        f.write(t)
    f.close()
    print 'perms_fact_apps_print end'


#########################
sql_perm_fact_perms = '''
SELECT app_id, perm_id, perm_individual, perm_lower FROM app_perm
'''
def perms_count_get(perm_list):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        if not perm_list.has_key(perm_id):
            perm_list[perm_id] = {}
            perm_list[perm_id]['app_id'] ={}
            perm_list[perm_id]['perm_lower'] = perm_lower
            print len(perm_list), perm_id, perm_lower, app_id
        if not perm_list[perm_id]['app_id'].has_key(app_id):
            perm_list[perm_id]['app_id'][app_id] = 0
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    #print apps
    return perm_list

    
def perms_count_get_print(perm_list):
    f = codecs.open('./txt/cm_perm_list_count.txt', 'w', encoding='utf-8')
    t = u'perm_id\tperm_lower\tapp_count\n'
    f.write(t)
    for perm_id in perm_list:
        perm_lower = perm_list[perm_id]['perm_lower']
        app_id = perm_list[perm_id]['app_id']
        app_count = len(app_id)
        t = u'%s\t%s\t%s\t\n'%(perm_id, perm_lower, app_count)
        f.write(t)
    f.close()
    print 'perms_fact_apps_print end'


##########################

if __name__ == '__main__':
    perm_list = {}
    #perm_list = perms_get(perm_list)
    #perms_get_print(perm_list)
    perm_list = {}
    perm_list = perms_count_get(perm_list)
    perms_count_get_print(perm_list)

    
