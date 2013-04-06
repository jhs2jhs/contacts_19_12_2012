#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *
from cm_contacts import *
from cm_perm_tidy import *
from cm_perm_fact import *
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

#######################################

def user_data_import(user_data_map, user_data_types):
    p = './txt/user_data_analysis_import.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        #print l
        ls = l.split('\t')
        p_id = ls[0].strip()
        p_label = ls[1].strip()
        p_opt = ls[2].strip().lower()
        data_type = ls[3].strip().lower()
        data_group = ls[4].strip().lower()
        if p_id == 'perm_id':
            l = f.readline()
            continue
        if p_opt.strip() == '':
            #print p_opt, ' p_opt'
            p_opt = 'none'
        #user_data_map
        if not user_data_map.has_key(p_id):
            user_data_map[p_id] = {}
        user_data_map[p_id]['p_label'] = p_label
        user_data_map[p_id]['p_opt'] = p_opt
        user_data_map[p_id]['data_type'] = data_type
        user_data_map[p_id]['data_group'] = data_group
        #user_data_types
        if not user_data_types.has_key(data_group):
            user_data_types[data_group] = {}
        if not user_data_types[data_group].has_key(data_type):
            user_data_types[data_group][data_type] = {}
        if data_type in ['connection_media', 'control']:
            p_opt = 'none'
        if not user_data_types[data_group][data_type].has_key(p_opt):
            user_data_types[data_group][data_type][p_opt] = {}
        user_data_types[data_group][data_type][p_opt][p_id] = 1
        l = f.readline()
    f.close()
    return user_data_map, user_data_types



def user_data_print(apps, categories, user_data_map, user_data_types):
    print 'user_data_print start'
    f = codecs.open('./txt_user_data/user_data.txt', 'w', encoding='utf-8')
    t = u'app_id\trank\tcategory\tcategory_id\tprice\trating_average\trating_total\tinstalls\tinstall_min\tinstall_max\tinstall_average\tdeveloper\tdeveloper_website\tdeveloper_email\tdeveloper_privacy\tyoutube_has\tyoutube_view_total\tgoogle_plus\taward_editor\taward_developer\ttheme_app\tperm_counts\t'
    for data_group in user_data_types:
        for data_type in user_data_types[data_group]:
            for p_opt in user_data_types[data_group][data_type]:
                t = u'%sd_%s_%s\t'%(t, data_type, p_opt)
            t = u'%sd_%s_%s\t'%(t, data_type, 'total')
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
        if not app.has_key('perms'):
            continue
        category = app['category'].lower().strip()
        category_id = categories[category]
        price = app['price']
        rating_average = app['rating_average']
        if float(rating_average) == 0:
            continue
        rating_total = app['rating_total']
        if float(rating_total) < 1:
            continue
        installs = app['installs']
        installs, install_min, install_max, install_average = installs_c(installs)
        if int(install_max) <= 6:
            continue
        #developer_href = app['developer']
        developer_website = app['developer_website']
        developer_email = app['developer_email']
        developer_privacy = app['developer_privacy']
        rank = -2
        if app.has_key('rank'):
            rank = app['rank']
        t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(app_id, rank, category, category_id, price, rating_average, rating_total, installs, install_min, install_max, install_average, developer_href, developer_website, developer_email, developer_privacy)
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
        award_editor = '0'
        award_developer = '0'
        if app.has_key('awards'):
            for award in app['awards']:
                award = award.strip().lower()
                if award == 'top developer':
                    award_developer = '1'
                if award == "editors' choice":
                    award_editor = '1'
        t = u'%s%s\t%s\t'%(t, award_editor, award_developer)
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
        for data_group in user_data_types:
            for data_type in user_data_types[data_group]:
                p_id_c_t = 0
                for p_opt in user_data_types[data_group][data_type]:
                    p_id_c = 0
                    for p_id in user_data_types[data_group][data_type][p_opt]:
                        if ps.has_key(p_id):
                            p_id_c = p_id_c + 1
                            p_id_c_t = p_id_c_t + 1
                    t = u'%s%s\t'%(t, p_id_c)
                t = u'%s%s\t'%(t, p_id_c_t)
        t = u'%s\n'%(t)
        f.write(t)
    f.close()
    print 'user_data_print end'
                            


#######################################
if __name__ == '__main__':
    p_maps = {}
    p_maps = p_map_import(p_maps)
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    apps = {}
    apps = perms_fact_perms_map(perm_maps, apps)
    apps = perms_fact_awards(apps)
    apps = perms_fact_apps(apps)
    apps = cm_contacts.contact_videos(apps)
    apps = cm_contacts.contact_share(apps)
    categories = category_get({})
    user_data_map = {}
    user_data_types = {}
    user_data_map, user_data_types = user_data_import(user_data_map, user_data_types)
    user_data_print(apps, categories, user_data_map, user_data_types)
    
