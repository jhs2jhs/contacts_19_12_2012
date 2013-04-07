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

# google p_id => google p_label
def p_map_import(p_maps):
    print '== p_map_import'
    p = './txt/perm_jian_input.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        #print l
        ls = l.split('\t')
        perm_id = ls[0].strip()
        perm_label = ls[2].strip()
        p_id = ls[3].strip()
        p_label = ls[4].strip()
        if not p_maps.has_key(p_id):
            p_maps[p_id] = p_label
        l = f.readline()
    f.close()
    return p_maps

#################
# # orignal perm_id => google perm_id
def perm_map_import(perm_maps):
    print '== perm_map_import'
    p = './txt/perm_jian_input.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        #print l
        ls = l.split('\t')
        perm_id = ls[0].strip()
        perm_label = ls[2].strip()
        p_id = ls[3].strip()
        p_label = ls[4].strip()
        if not perm_maps.has_key(perm_id):
            perm_maps[perm_id] = {}
        perm_maps[perm_id]['perm_label'] = perm_label
        perm_maps[perm_id]['p_id'] = p_id
        perm_maps[perm_id]['p_label'] = p_label
        l = f.readline()
    f.close()
    return perm_maps

def user_data_import(user_data_map):
    p = './txt/user_data_analysis_out.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        #print l
        ls = l.split('\t')
        p_id = ls[0].strip()
        p_label = ls[1].strip()
        p_operation = ls[2].strip()
        if p_operation.strip() == '':
            print p_operation, ' p_operation'
            p_operation = 'NONE'
        p_category = ls[3]
        if not user_data_map.has_key(p_id):
            user_data_map[p_id] = {}
        user_data_map[p_id]['p_label'] = p_label
        user_data_map[p_id]['p_operation'] = p_operation
        user_data_map[p_id]['p_category'] = p_category
        l = f.readline()
    f.close()
    return user_data_map

#################
sql_perm_fact_perms = '''
SELECT app_id, perm_id, perm_individual, perm_lower FROM app_perm
'''
def perms_map_get(perm_maps, p_list):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    #p_list = {}
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        p_id = perm_maps[perm_id]['p_id']
        p_label = perm_maps[perm_id]['p_label']
        if not p_list.has_key(p_id):
            p_list[p_id] = {}
            p_list[p_id]['p_label'] = p_label
            p_list[p_id]['app_ids'] = {}
        if not p_list[p_id]['app_ids'].has_key(app_id):
            p_list[p_id]['app_ids'][app_id] = 1
        else:
            p_list[p_id]['app_ids'][app_id] =  p_list[p_id]['app_ids'][app_id] + 1
            if p_list[p_id]['app_ids'][app_id] > 3:
                print '==', p_list[p_id]['app_ids'][app_id], p_id, p_label, perm_id, perm_lower, app_id
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    #print apps
    return p_list


def user_data_get(perm_maps, user_data_map, p_list):
    print 'perm_fact_perms start'
    c = db.cursor()
    c.execute(sql_perm_fact_perms, ())
    r = c.fetchone()
    #p_list = {}
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm_id = r[1]
        perm_lower = r[3]
        p_id = perm_maps[perm_id]['p_id']
        p_category = user_data_map[p_id]['p_category']
        p_label = user_data_map[p_id]['p_label']
        p_operation = user_data_map[p_id]['p_operation']
        if not p_list.has_key(p_category):
            p_list[p_category] = {}
        if not p_list[p_category].has_key(p_operation):
            p_list[p_category][p_operation] = {}
            p_list[p_category][p_operation]['app_ids'] = {}
        if not p_list[p_category][p_operation].has_key(p_id):
            p_list[p_category][p_operation][p_id] = {}
            p_list[p_category][p_operation][p_id]['p_label'] = p_label
            p_list[p_category][p_operation][p_id]['app_ids'] = {}
        #print p_list[p_category][p_operation]
        #print p_list[p_category], p_operation, app_id
        if not p_list[p_category][p_operation][p_id]['app_ids'].has_key(app_id):
            p_list[p_category][p_operation][p_id]['app_ids'][app_id] = 1
        else:
            p_list[p_category][p_operation][p_id]['app_ids'][app_id] =  p_list[p_category][p_operation][p_id]['app_ids'][app_id] + 1
            if p_list[p_category][p_operation][p_id]['app_ids'][app_id] > 10:
                print '== simple ', p_list[p_category][p_operation][p_id]['app_ids'][app_id], p_id, p_label, perm_id, perm_lower, app_id, p_category, p_operation
        if not p_list[p_category][p_operation]['app_ids'].has_key(app_id):
            p_list[p_category][p_operation]['app_ids'][app_id] = 1
        else:
            p_list[p_category][p_operation]['app_ids'][app_id] =  p_list[p_category][p_operation]['app_ids'][app_id] + 1
            if p_list[p_category][p_operation]['app_ids'][app_id] > 10:
                print '== full ', p_list[p_category][p_operation]['app_ids'][app_id], p_id, p_label, perm_id, perm_lower, app_id, p_category, p_operation
        r = c.fetchone()
    c.close()
    print 'perm_fact_perms end'
    #print apps
    return p_list

##################

def perms_map_get_count_print(p_list):
    f = codecs.open('./txt/cm_perm_maps_count.txt', 'w', encoding='utf-8')
    t = u'p_id\tp_label\tapp_count\n'
    f.write(t)
    for p_id in p_list:
        perm = p_list[p_id]
        p_label = perm['p_label']
        app_counts = len(perm['app_ids'])
        t = u'%s\t%s\t%s\t\n'%(p_id, p_label, app_counts)
        f.write(t)
    f.close()
    print 'perms_fact_apps_print end'

def user_data_get_count_print(p_list):
    f = codecs.open('./txt/user_data_analysis_count_simple.txt', 'w', encoding='utf-8')
    t = u'p_category\tp_operation\tapp_count\n'
    f.write(t)
    f1 = codecs.open('./txt/user_data_analysis_count_full.txt', 'w', encoding='utf-8')
    t1 = u'p_category\tp_operation\tp_id\tp_label\tapp_count\n'
    f1.write(t1)
    for p_category in p_list:
        for p_operation in p_list[p_category]:
            perm = p_list[p_category][p_operation]
            app_counts = len(perm['app_ids'])
            t = u'%s\t%s\t%s\t\n'%(p_category, p_operation, app_counts)
            f.write(t)
            for p_id in p_list[p_category][p_operation]:
                if p_id == 'app_ids':
                    continue
                perm = p_list[p_category][p_operation][p_id]
                p_label = perm['p_label']
                app_counts = len(perm['app_ids'])
                t1 = u'%s\t%s\t%s\t%s\t%s\t\n'%(p_category, p_operation, p_id, p_label, app_counts)
                f1.write(t1)
    f.close()
    f1.close()
    print 'perms_fact_apps_print end'


if __name__ == '__main__':
    #p_list = {}
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    #p_list = perms_map_get(perm_maps, p_list)
    #perms_map_get_count_print(p_list)
    p_list = {}
    user_data_map = {}
    user_data_map = user_data_import(user_data_map)
    p_list = user_data_get(perm_maps, user_data_map, p_list)
    user_data_get_count_print(p_list)
    
    
    
