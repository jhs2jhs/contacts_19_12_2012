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

def perm_table(apps, apps_t):
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 10)
        app = apps[app_id]
        if not app.has_key('perms'):
            continue
        if not app.has_key('price') or not app.has_key('perms'):
            continue
        price = app['price']
        if price == '0':
            price = 'free'
        else:
            price = 'paid'
        award_editor = 'no'
        award_developer = 'no'
        if app.has_key('awards'):
            for award in app['awards']:
                award = award.strip().lower()
                if award == 'top developer':
                    award_developer = 'yes'
                if award == "editors' choice":
                    award_editor = 'yes'
        category = app['category']
        perms = app['perms']
        for p_id in perms:
            if not apps_t.has_key(p_id):
                apps_t[p_id] = {}
            if not apps_t[p_id].has_key(price):
                apps_t[p_id][price] = {}
            if not apps_t[p_id][price].has_key(category):
                apps_t[p_id][price][category] = {}
            if not apps_t[p_id][price][category].has_key(award_editor):
                apps_t[p_id][price][category][award_editor] = {}
            if not apps_t[p_id][price][category][award_editor].has_key(app_id):
                apps_t[p_id][price][category][award_editor][app_id] = {}
                apps_t[p_id][price][category][award_editor][app_id]['apps'] = app
                apps_t[p_id][price][category][award_editor][app_id]['apps_count'] = 1
            else:
                apps_t[p_id][price][category][award_editor][app_id]['apps_count'] = apps_t[p_id][price][category][award_editor][app_id]['apps_count'] + 1
    return apps_t
     
def perm_table_print(apps_t, categories, p_maps):
    t = u'p_id\tp_label\t'
    for cate in categories:
        cate_id = categories[cate]
        t = u'%s%s_%s\t'%(t, str(cate_id), str(cate))
    t = u'%s\n'%(t)
    f_free = codecs.open('./txt/paper_matt_privacy_free.txt', 'w', encoding='utf-8')
    f_paid = codecs.open('./txt/paper_matt_privacy_paid.txt', 'w', encoding='utf-8')
    f_free.write(t)
    f_paid.write(t)
    f_total = codecs.open('./txt/paper_matt_privacy_total.txt', 'w', encoding='utf-8')
    f_total.write(t)
    total_f = {}
    for p_id in p_maps:
        p_label = p_maps[p_id]
        if not apps_t.has_key(p_id):
            continue
        if not total_f.has_key(p_id):
            total_f[p_id] = {}
        for price in ['free', 'paid']:
            t = u'%s\t%s\t'%(p_id, p_label)
            for cate in categories:
                if not total_f[p_id].has_key(cate):
                    total_f[p_id][cate] = {'free':'none', 'paid':'none'}
                if not apps_t[p_id].has_key(price):
                    #t = u'%s%s\t'%(t, 'none')
                    cate_award_f = 'none'
                    cate_award_ff = 'none'
                else:
                    cate_id = categories[cate]
                    if not apps_t[p_id][price].has_key(cate):
                        cate_award_f = 'none'
                        cate_award_ff = 'none'
                    else:
                        award_editor_yes_len = 0
                        award_editor_no_len = 0
                        if apps_t[p_id][price][cate].has_key('yes'):
                            award_editor_yes = apps_t[p_id][price][cate]['yes']
                            award_editor_yes_len = len(award_editor_yes)
                        if apps_t[p_id][price][cate].has_key('no'):
                            award_editor_no = apps_t[p_id][price][cate]['no']
                            award_editor_no_len = len(award_editor_no)
                        if award_editor_yes_len > 0 and award_editor_no_len > 0:
                            cate_award_f = '1_%d_%d'%(len(award_editor_yes), len(award_editor_no))
                            cate_award_ff = '1'
                        if award_editor_yes_len == 0 and award_editor_no_len > 0:
                            cate_award_f = '2_0_%d'%(len(award_editor_no))
                            cate_award_ff = '2'
                        if award_editor_yes_len > 0 and award_editor_no_len == 0:
                            cate_award_f = '0_%d_0'%(len(award_editor_yes))
                            cate_award_ff = '0'
                            print '0_', 
                        if award_editor_yes_len == 0 and award_editor_no_len == 0:
                            print 'both == 0', p_id, category, price
                            cate_award_f = 'none'
                    t = u'%s%s\t'%(t, cate_award_f)
                    if price == 'free':
                        total_f[p_id][cate]['free'] = cate_award_f
                    if price == 'paid':
                        total_f[p_id][cate]['paid'] = cate_award_f
            t = u'%s\n'%(t)
            if price == 'free':
                f_free.write(t)
            if price == 'paid':
                f_paid.write(t)
    f_free.close()
    f_paid.close()
    ##
    for p_id in total_f:
        p_label = p_maps[p_id]
        t = u'%s\t%s\t'%(p_id, p_label)
        for cate in categories:
            free_f = 'none'
            paid_f = 'none'
            if total_f[p_id].has_key(cate):
                if total_f[p_id][cate].has_key('free'):
                    free_f = total_f[p_id][cate]['free']
                if total_f[p_id][cate].has_key('paid'):
                    paid_f = total_f[p_id][cate]['paid']
            t = u'%s%s_+_%s\t'%(t, free_f, paid_f)
        t = u'%s\n'%(t)
        f_total.write(t)
    f_total.close()
    
            
########################################
if __name__ == '__main__':
    p_maps = {}
    p_maps = p_map_import(p_maps)
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    apps = {}
    apps = perms_fact_perms_map(perm_maps, apps)
    apps = perms_fact_awards(apps)
    apps = perms_fact_apps(apps)
    #apps = cm_contacts.contact_videos(apps)
    #apps = cm_contacts.contact_share(apps)
    apps_t = {}
    apps_t = perm_table(apps, apps_t)
    categories = category_get({})
    perm_table_print(apps_t, categories, p_maps)
