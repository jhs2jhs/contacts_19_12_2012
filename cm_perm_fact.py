#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *
from cm_contacts import *
from cm_perm_tidy import *
from cm_perm_maps import *

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
def perms_fact_perms_map(perm_maps, apps):
    print 'perm_fact_perms_map start'
    c = db.cursor()
    print sql_perm_fact_perms
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        p_id = perm_maps[perm_id]['p_id']
        p_label = perm_maps[perm_id]['p_label']
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('perms'):
            apps[app_id]['perms'] = {}
        if apps[app_id]['perms'].has_key(p_id):
            apps[app_id]['perms'][p_id] = apps[app_id]['perms'][p_id] + 1
            if apps[app_id]['perms'][p_id] > 3:
                print 'perm_fact_perms > 3', app_id, p_id, apps[app_id]['perms'][p_id]
        else:
            apps[app_id]['perms'][p_id] = 1
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms_map end'
    #print apps
    return apps

#sql_perm_fact_perms = '''
#SELECT app_id, perm_id, perm_individual, perm_lower FROM app_perm
#'''
def perms_fact_perms(apps):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('perms'):
            apps[app_id]['perms'] = {}
            apps[app_id]['contact_perms'] = {}
        if apps[app_id]['perms'].has_key(perm_id):
            apps[app_id]['perms'][perm_id] = apps[app_id]['perms'][perm_id] + 1
            if apps[app_id]['perms'][perm_id] > 1:
                print 'perm_fact_perms > 1', app_id, perm_id, apps[app_id]['perms'][perm_id]
        else:
            apps[app_id]['perms'][perm_id] = 1
        if int(perm_id) in [225, 77, 139, 140, 161, 172, 173, 174, 174, 230, 175, 231]:
            apps[app_id]['contact_perms'][perm_id] = 1
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    #print apps
    return apps

#################

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

    
# do not have rating_0 - rating_5
sql_perm_fact_apps = '''
SELECT app_id, developer_href, category, price, rating_average, rating_total, installs, 
developer_website, developer_email, developer_privacy, title, desc 
FROM app WHERE developer_href IS NOT NULL 
'''
def perms_fact_apps(apps):
    print 'perm_fact_apps start'
    c = db.cursor()
    c.execute(sql_perm_fact_apps, ())
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        developer_href = r[1].encode('utf-8').lower().strip()
        category = r[2].encode('utf-8').lower().strip()
        if category == 'arcade & action':
            category = 'arcade and action'
        if category == 'cards & casino':
            category = 'cards and casino'
        price = r[3].encode('utf-8').lower().strip()
        price = price_c(price)
        rating_average = r[4].replace(',','').encode('utf-8').lower().strip()
        rating_average = check_none(rating_average, '0')
        rating_total = r[5].replace(',','').encode('utf-8').lower().strip()
        rating_total = check_none(rating_total, '0')
        installs = r[6].encode('utf-8').lower().strip()
        installs = check_none(installs, '')
        if not apps.has_key(app_id):
            apps[app_id] = {}
        apps[app_id]['developer'] = developer_href
        apps[app_id]['category'] = category ## category_id should be assigned later
        apps[app_id]['price'] = price
        apps[app_id]['rating_average'] = rating_average
        apps[app_id]['rating_total'] = rating_total
        apps[app_id]['installs'] = installs
        dev_website = r[7].encode('utf-8').strip()
        dev_email = r[8].encode('utf-8').strip()
        dev_privacy = r[9].encode('utf-8').strip()
        apps[app_id]['developer_website'] = yes_no_num(dev_website)
        apps[app_id]['developer_email'] = yes_no_num(dev_email)
        apps[app_id]['developer_privacy'] = yes_no_num(dev_privacy)
        # if it is a theme app, from title, or app_id, or description.
        # count of permission. 
        app_title = r[10].encode('utf-8').strip().lower()
        app_desc = r[11].encode('utf-8').strip().lower()
        apps[app_id]['theme_app'] = '0'
        if u'theme' in app_id or 'wallpaper' in app_id:
            apps[app_id]['theme_app'] = '1'
        if u'theme' in app_title or u'wallpaper' in app_title:
            apps[app_id]['theme_app'] = '2'
        if u'theme' in app_desc or u'wallpaper' in app_desc :
            apps[app_id]['theme_app'] = '3'
        apps[app_id]['app_title'] = app_title
        r = c.fetchone()
    c.close()
    print 'perms_fact_apps end', len(apps)
    return apps
    
#def perms_fact_apps_print(apps, perms, categories):
def perms_fact_apps_print(apps, categories, p_maps):
    #f1 = codecs.open('./txt/cm_perm_fact_network.txt', 'w', encoding='utf-8')
    #f1.write('app_id\tcategory_id\tcategory\tperm_id\tperm\tprice\tinstalls\tawards\n')
    f = codecs.open('./txt/cm_perm_fact_apps.txt', 'w', encoding='utf-8')
    t = u'app_id\tcategory\tcategory_id\tprice\trating_average\trating_total\tinstalls\tinstall_min\tinstall_max\tinstall_average\tdeveloper\tdeveloper_website\tdeveloper_email\tdeveloper_privacy\tyoutube_has\tyoutube_view_total\tgoogle_plus\tawards\tawards_type\tawards_count\ttheme_app\tperm_counts\t'
    ''' perm code index system using in jian's original dataset
    for perm_id in perms:
        perm_lower = perms[perm_id]
        t = u'%sp_%s\t'%(t, perm_id)
    '''
    for p_id in p_maps: # perm code index system usng google default one
        p_label = p_maps[p_id]
        t = u'%sp_%s\t'%(t, str(p_id))
    t = u'%s\n'%(t)
    f.write(t)
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 10)
        app = apps[app_id]
        if not app.has_key('developer'):
            continue
        developer_href = app['developer']
        if developer_href == '' or developer_href == None:
            continue
        t = u'%s\t'%(app_id)
        category = app['category'].lower().strip()
        category_id = categories[category]
        price = app['price']
        rating_average = app['rating_average']
        rating_total = app['rating_total']
        installs = app['installs']
        installs, install_min, install_max, install_average = installs_c(installs)
        developer_href = app['developer']
        developer_website = app['developer_website']
        developer_email = app['developer_email']
        developer_privacy = app['developer_privacy']
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(t, category, category_id, price, rating_average, rating_total, installs, install_min, install_max, install_average, developer_href, developer_website, developer_email, developer_privacy)
        if app.has_key('youtube'):
            youtube_has = '1'
            youtube_view_total = check_none(app['youtube']['view_total'], '0')
        else:
            youtube_has = '0'
            youtube_view_total = 'none'
        t = u'%s%s\t%s\t'%(t, youtube_has, youtube_view_total)
        if app.has_key('share'):
            google_plus_figure = check_none(app['share']['google_plus'], '0')
        else:
            google_plus_figure = 'none'
        t = u'%s%s\t'%(t, google_plus_figure)
        app_awards = ''
        app_awards_count = 0
        if not app.has_key('awards'):
            t = u'%s%s\t%s\t'%(t, '0', '0')
            app_awards = 'none'
            app_awards_count = 0
        else:
            awards = app['awards']
            for award in awards:
                t = u'%s%s+'%(t, award)
                app_awards = '%s&%s'%(app_awards, award)
                app_awards_count = app_awards_count + 1
            t = u'%s\t1\t'%(t)
        t = u'%s%s\t'%(t, str(app_awards_count))
        theme_app = app['theme_app']
        t = u'%s%s\t'%(t, theme_app)
        if not app.has_key('perms'):
            ps = {}
            perm_counts = 0
        else: 
            ps = app['perms']
            perm_counts = len(ps)
            #print ps
        t = u'%s%s\t'%(t, str(perm_counts))
        ''' perm code system: jian's orignal 
        for perm_id in perms:
            perm_lower = perms[perm_id]
            flag = '0' # false
            #print flag, ps.has_key(str(perm_id)), perm_id, perm_lower, ps
            if ps.has_key(str(perm_id)):
                flag = '1' # true
                f1.write(u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(app_id, category_id, category, perm_id, perm_lower, price, installs, app_awards))
            t = u'%s%s\t'%(t, flag)
        '''
        for p_id in p_maps: # perm code system: google defined default
            flag = '0'
            if ps.has_key(p_id):
                flag = '1'
                #f1.write(u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(app_id, category_id, category, perm_id, perm_lower, price, installs, app_awards))
            t = u'%s%s\t'%(t, flag)
        t = u'%s\n'%(t)
        f.write(t)
    #f1.close()
    f.close()
    print 'perms_fact_apps_print end'
            
##############################
##############################

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
    for perm_id in perms:
        perm_lower = perms[perm_id]
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
        for perm_id in perms:
            perm_lower = perms[perm_id]
            flag = '0'
            if ps.has_key(str(perm_id)):
                flag = '1'
            t = u'%s%s\t'%(t, flag)
        t = u'%s\n'%(t)
        f.write(t)
    f.close()
    print 'perms_fact_developers_print end '
    

##########################

if __name__ == '__main__':
    p_maps = {}
    p_maps = p_map_import(p_maps)
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    apps = {}
    apps = perms_fact_perms_map(perm_maps, apps)
    #apps = {}
    #apps = perms_fact_perms_maps(apps)
    apps = perms_fact_awards(apps)
    apps = perms_fact_apps(apps)
    apps = cm_contacts.contact_videos(apps)
    apps = cm_contacts.contact_share(apps)
    categories = category_get({})
    #perms = perms_get({})
    #perms_fact_apps_print(apps, perms, categories)
    perms_fact_apps_print(apps, categories, p_maps)
    ##
    #developers = {}
    #developers = perms_fact_developers(apps, developers)
    #perms_fact_developers_print(developers)
    #print developers
    
