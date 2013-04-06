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
'''
1. get category array from excel table 1: categories = {1:'books & reference', 2: "sports & games", ...., 30:'racing' }
2. get permission array from excel table 1: perms = {p_4:'WRITE_EXTERNAL_STORAGE', ..., P_7:""}, also need to lable whether this permission is in freemium, paid or operation. 
3. get illegitimate permission list for each category from permission. like p1c30 has [p_38, p_96, ...].
4. get perm for all_category from free_all_classes and paid_all_classes excel for each permission: 
5. get perm score for each category from centr_pxcx.txt: 
6. calculate standard derivation for each subcategory: double check whether need to delete certian permission in advanced. 
7. calculate the deviance score for each permission in each category. 
8. calculate the count of deviance score for each app. 
9. calculate the count of deviance score for each developer. 
'''

##########################################

def import_category_desc(categories):
    print 'import_category_desc start'
    p = './txt_centr/category_desc.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        ls = l.split('\t')
        c_id = ls[0].strip().lower()
        if c_id == '':
            l = f.readline()
            continue
        c_label = ls[1].strip()
        if not categories.has_key(c_id):
            categories[c_id] = c_label
        l = f.readline()
    f.close()
    print 'import_category_desc end'
    return categories

def import_perm_desc_type(perms):
    print 'import_perm_desc_type start'
    p = './txt_centr/perm_desc_type.txt'
    f = open(p, 'r')
    l = f.readline()
    while l:
        ls = l.split('\t')
        p_id = ls[0].strip().lower()
        if p_id == '':
            l = f.readline()
            continue
        p_label = ls[1].strip()
        p_type = ls[2].strip().lower()
        if not perms.has_key(p_id):
            perms[p_id] = {}
        perms[p_id]['label'] = p_label
        perms[p_id]['type'] = p_type
        l = f.readline()
    f.close()
    print 'import_perm_desc_type end'
    return perms


def import_illegimate_free(illegimates, fp_type):
    print 'import_illegimate_%s start'%(fp_type)
    p = './txt_centr/illegimate_%s.txt'%(fp_type)
    f = open(p, 'r')
    l = f.readline()
    while l:
        ls = l.split('\t')
        p_id = ls[0].strip().lower()
        if p_id == '':
            l = f.readline()
            continue
        i = 0
        #print p_id, 
        for cate in ls[1:]:
            i = i + 1
            c_id = u'%s'%(i)
            if not illegimates.has_key(c_id):
                illegimates[c_id] = {}
            if not illegimates[c_id].has_key(fp_type):
                illegimates[c_id][fp_type] = {}
            cate = cate.lower().strip()
            if cate == '':
                cate = 'none'
            illegimates[c_id][fp_type][p_id] = cate
            #if cate == '2':
            #    print cate, 
        print 
        l = f.readline()
    f.close()
    print 'import_illegimate_%s end'%(fp_type)
    return illegimates

def import_all_classes(perms_all_classess, fp_type):
    print 'import_%s_all_classes start'%(fp_type)
    p = './txt_centr/%s_all_classes.txt'%(fp_type)
    f = open(p, 'r')
    l = f.readline()
    l = f.readline()
    while l:
        ls = l.split(',')
        p_id = ls[0].strip().lower()
        if p_id == '':
            l = f.readline()
            continue
        degree = ls[1].lower().strip()
        closeness = ls[2].lower().strip()
        betweenness = ls[3].lower().strip()
        if not perms_all_classess.has_key(p_id):
            perms_all_classess[p_id] = {}
        if not perms_all_classess[p_id].has_key(fp_type):
            perms_all_classess[p_id][fp_type] = {}
        perms_all_classess[p_id][fp_type]['degree'] = float(degree)
        perms_all_classess[p_id][fp_type]['closeness'] = float(closeness)
        perms_all_classess[p_id][fp_type]['betweenness'] = float(betweenness)
        l = f.readline()
    f.close()
    print 'import_%s_all_classess end'%(fp_type)
    return perms_all_classess


def import_picj(perms_picj, fp_type, c_id):
    print 'import_p%sc%s start'%(str(fp_type), str(c_id))
    p = './txt_centr/picj/centr_p%sc%s.txt'%(str(fp_type), str(c_id))
    f = open(p, 'r')
    l = f.readline()
    l = f.readline()
    while l:
        ls = l.split(',')
        p_id = ls[0].strip().lower()
        if p_id == '':
            l = f.readline()
            continue
        degree = ls[1].lower().strip()
        closeness = ls[2].lower().strip()
        betweenness = ls[3].lower().strip()
        if not perms_picj.has_key(c_id):
            perms_picj[c_id] = {}
        if not perms_picj[c_id].has_key(fp_type):
            perms_picj[c_id][fp_type] = {}
        if not perms_picj[c_id][fp_type].has_key(p_id):
            perms_picj[c_id][fp_type][p_id] = {}
        perms_picj[c_id][fp_type][p_id]['degree'] = float(degree)
        perms_picj[c_id][fp_type][p_id]['closeness'] = float(closeness)
        perms_picj[c_id][fp_type][p_id]['betweenness'] = float(betweenness)
        l = f.readline()
    f.close()
    print 'import_p%sc%s end'%(str(fp_type), str(c_id))
    return perms_picj

def import_picj_loop(perms_picj, categories):
    for fp_type in ['1', '2']:
        for c_id in categories:
            perms_picj = import_picj(perms_picj, fp_type, c_id)
    return perms_picj

import numpy
def get_stdev(perms_picj, categories):
    for fp_type in ['1', '2']:
        for c_id in categories:
            degrees = []
            closenesss = []
            betweennesss = []
            for p_id in perms_picj[c_id][fp_type]:
                degree = perms_picj[c_id][fp_type][p_id]['degree']
                closeness = perms_picj[c_id][fp_type][p_id]['closeness']
                betweenness = perms_picj[c_id][fp_type][p_id]['betweenness']
                degrees.append(degree)
                closenesss.append(closeness)
                betweennesss.append(betweenness)
            stddev_d = numpy.array(degrees).std()
            stddev_c = numpy.array(closenesss).std()
            stddev_b = numpy.array(betweennesss).std()
            perms_picj[c_id][fp_type]['stddev_d'] = stddev_d
            perms_picj[c_id][fp_type]['stddev_c'] = stddev_c
            perms_picj[c_id][fp_type]['stddev_b'] = stddev_b
            if c_id == '30':
                print stddev_d,  stddev_c, stddev_b
    return perms_picj
            

def get_deviance(perms_picj, categories, perms, illegimates):
    fs = {}
    for fp_type in ['1', '2']:
        for c_id in categories:
            if not fs.has_key(c_id):
                fs[c_id] = {}
            if not fs[c_id].has_key(fp_type):
                fs[c_id][fp_type] =  codecs.open('./txt_centr/picj_o/d_p%sc%s.txt'%(fp_type, c_id), 'w', encoding='utf-8')
                fs[c_id][fp_type].write(u'p_id\td_degree\td_closeness\td_betweenness\tillegimate_type\tp_label\tp_type\tabsence\n')
    for p_id in perms_all_classess:
        pid = p_id.split('_')[1].strip()
        pid = int(pid)
        #if pid in [29, 36, 39, 41, 50, 52, 54, 57, 58, 60, 62, 63, 65, 68, 69, 71, 72, 73, 75, 79, 80, 82, 85, 86, 87, 88, 89, 90, 93, 94, 95, 97, 98, 99]:
        #    continue
        p_label = 'none'
        p_type = 'other'
        if perms.has_key(p_id):
            p_label = perms[p_id]['label']
            p_type = perms[p_id]['type']
        for fp_type in ['1', '2']:
            for c_id in categories:
                #print c_id, fp_type, p_id
                #print perms_picj[c_id]
                #print perms_picj[c_id][fp_type]
                is_illegimate = '0'
                if illegimates.has_key(c_id) and illegimates[c_id].has_key(fp_type) and illegimates[c_id][fp_type].has_key(p_id):
                    #print illegimates[c_id][fp_type][p_id]
                    is_illegimate = illegimates[c_id][fp_type][p_id]
                stddev_d = perms_picj[c_id][fp_type]['stddev_d']
                stddev_c = perms_picj[c_id][fp_type]['stddev_c']
                stddev_b = perms_picj[c_id][fp_type]['stddev_b']
                if not perms_all_classess[p_id].has_key(fp_type):
                    #print p_id, fp_type
                    continue
                all_d = perms_all_classess[p_id][fp_type]['degree']
                all_c = perms_all_classess[p_id][fp_type]['closeness']
                all_b = perms_all_classess[p_id][fp_type]['betweenness']
                if not perms_picj[c_id][fp_type].has_key(p_id): ## need to double check p2c29 why does not have value. and there are many other values. 
                    #print '############', c_id, fp_type, p_id, p_type, p_label, is_illegimate
                    d = 0
                    c = 0
                    b = 0
                    absence = 'yes'
                else:
                    d = perms_picj[c_id][fp_type][p_id]['degree']
                    c = perms_picj[c_id][fp_type][p_id]['closeness']
                    b = perms_picj[c_id][fp_type][p_id]['betweenness']
                    absence = 'no'
                deviance_d = (d - all_d)/stddev_d
                deviance_c = (c - all_c)/stddev_c
                deviance_b = (b - all_b)/stddev_b
                #print deviance_d, deviance_c, deviance_b
                t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(p_id, deviance_d, deviance_c, deviance_b, is_illegimate, p_label, p_type, absence)
                fs[c_id][fp_type].write(t)
    for c_id in fs:
        for fp_type in fs[c_id]:
            fs[c_id][fp_type].close()
                

if __name__ == '__main__':
    categories = {}
    categories = import_category_desc(categories)
    perms = {}
    perms = import_perm_desc_type(perms)
    #print perms
    #print 
    #print categories
    illegimates = {}
    illegimates = import_illegimate_free(illegimates, '1')
    illegimates = import_illegimate_free(illegimates, '2')
    print illegimates
    perms_all_classess = {}
    perms_all_classess = import_all_classes(perms_all_classess, '1')
    perms_all_classess = import_all_classes(perms_all_classess, '2')
    print perms_all_classess
    perms_picj = {}
    perms_picj = import_picj_loop(perms_picj, categories)
    perms_picj = get_stdev(perms_picj, categories)
    #print perms_picj
    get_deviance(perms_picj, categories, perms, illegimates)
