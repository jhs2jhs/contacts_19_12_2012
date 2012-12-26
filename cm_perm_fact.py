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

sql_perm_fact_perms = '''
SELECT app_id, perm_individual FROM permission
'''
def perms_fact_perms(apps, perms):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm = r[1].encode('utf-8').lower().strip()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('perms'):
            apps[app_id]['perms'] = {}
        if not perms.has_key(perm):
            perms[perm] = 'p_'+str(len(perms)+1)
        perm_id = perms[perm]
        if apps[app_id]['perms'].has_key(perm_id):
            apps[app_id]['perms'][perm_id] = apps[app_id]['perms'][perm_id] + 1
        else:
            apps[app_id]['perms'][perm_id] = 1
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    return apps, perms


sql_perm_fact_awards = '''
SELECT app_id, award from awards
'''
def perms_fact_awards(apps):
    print 'perm_fact_awards start'
    c = db.cursor()
    c.execute(sql_perm_fact_awards, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        award = r[1].encode('utf-8').lower().strip()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('awards'):
            apps[app_id]['awards'] = {}
        apps[app_id]['awards'][award] = 1
        r = c.fetchone()
    print 'perm_fact_awards end'
    return apps

    
sql_perm_fact_apps = '''
SELECT app_id, developer_href FROM app WHERE developer_href IS NOT NULL
'''
def perms_fact_apps(apps):
    print 'perm_fact_apps start'
    c = db.cursor()
    c.execute(sql_perm_fact_apps, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        developer_href = r[1].encode('utf-8').lower().strip()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        apps[app_id]['developer'] = developer_href
        r = c.fetchone()
    c.close()
    print 'perms_fact_apps end'
    return apps
                                          

def perms_fact_perms_print(perms):
    print 'perm_fact_perms_print start'
    f = codecs.open('./txt/cm_perm_fact_perms.txt', 'w', encoding='utf-8')
    f.write('perm_id\tperm_lable\n')
    for perm in perms:
        perm_id = perms[perm]
        t = u'%s\t%s\t\n'%(perm_id, perm)
        f.write(t)
    f.close()
    print 'perms_fact_perms_print end'
                                          
    
def perms_fact_apps_print(apps, perms):
    f = codecs.open('./txt/cm_perm_fact_apps.txt', 'w', encoding='utf-8')
    t = u'app_id\tawards\t'
    for perm in perms:
        perm_id = perms[perm]
        t = u'%s%s\t'%(t, perm_id)
    t = u'%s\n'%(t)
    f.write(t)
    for app_id in apps:
        app = apps[app_id]
        if not app.has_key('developer'):
            continue
        developer_href = app['developer']
        if developer_href == '' or developer_href == None:
            continue
        t = u'%s\t'%(app_id)
        if not app.has_key('awards'):
            t = u'%s%s\t'%(t, 'none')
        else:
            awards = app['awards']
            for award in awards:
                t = u'%s%s+'%(t, award)
            t = u'%s\t'%(t)
        if not app.has_key('perms'):
            ps = {}
        else: 
            ps = app['perms']
            #print ps
        for perm in perms:
            perm_id = perms[perm]
            flag = '0' # false
            if ps.has_key(perm_id):
                flag = '1' # true
            t = u'%s%s\t'%(t, flag)
        t = u'%s\n'%(t)
        f.write(t)
    f.close()
    print 'perms_fact_apps_print end'
            

def perms_fact_developers(apps, developers):
    print 'perms_fact_developers start'
    for app_id in apps:
        app = apps[app_id]
        if not app.has_key('developer'):
            continue
        developer_href = app['developer']
        if developer_href == '' or developer_href == None:
            continue
        if not app.has_key('perms'):
            continue
        if not developers.has_key(developer_href):
            developers[developer_href] = {}
        if app.has_key('awards'):
            for award in app['awards']:
                if not developers[developer_href].has_key('awards'):
                    developers[developer_href]['awards'] = {}
                if not developers[developer_href]['awards'].has_key(award):
                    developers[developer_href]['awards'][award] = 1
                else:
                    developers[developer_href]['awards'][award] = developers[developer_href]['awards'][award] + 1
        perms = app['perms']
        if not developers[developer_href].has_key('perms'):
            developers[developer_href]['perms'] = {}
        for perm_id in perms:
            if not developers[developer_href]['perms'].has_key(perm_id):
                developers[developer_href]['perms'][perm_id] = 1
            else:
                developers[developer_href]['perms'][perm_id] = developers[developer_href]['perms'][perm_id] + 1
        if developers[developer_href].has_key('apps_count'):
            developers[developer_href]['apps_count'] = developers[developer_href]['apps_count'] + 1
        else:
            developers[developer_href]['apps_count'] = 1
    print 'perms_fact_developers end'
    return developers

def perms_fact_developers_print(developers):
    print 'perms_fact_developers_print start'
    f = codecs.open('./txt/cm_perm_fact_developers.txt', 'w', encoding='utf-8')
    t = u'developer_href\tapps_count\tawards\t'
    for perm in perms:
        perm_id = perms[perm]
        t = u'%s%s\t'%(t, perm_id)
    t = u'%s\n'%(t)
    f.write(t)
    for developer_href in developers:
        dev = developers[developer_href]
        apps_count = dev['apps_count']
        t = u'%s\t%s\t'%(developer_href, unicode(apps_count))
        if dev.has_key('awards'):
            awards = dev['awards']
            for award in awards:
                award_count = awards[award]
                t = u'%s%s_%s+'%(t, award, unicode(award_count))
            t = u'%s\t'%(t)
        else:
            t = u'%s%s\t'%(t, 'none')
        if not dev.has_key('perms'):
            ps = {}
        else:
            ps = dev['perms']
        for perm in perms:
            perm_id = perms[perm]
            flag = '0'
            if ps.has_key(perm_id):
                flag = '1'
            t = u'%s%s\t'%(t, flag)
        t = u'%s\n'%(t)
        f.write(t)
    f.close()
    print 'perms_fact_developers_print end '
    

if __name__ == '__main__':
    apps = {}
    perms = {}
    apps, perms = perms_fact_perms(apps, perms)
    apps = perms_fact_awards(apps)
    apps = perms_fact_apps(apps)
    perms_fact_perms_print(perms)
    perms_fact_apps_print(apps, perms)
    developers = {}
    developers = perms_fact_developers(apps, developers)
    perms_fact_developers_print(developers)
    #print developers
    
