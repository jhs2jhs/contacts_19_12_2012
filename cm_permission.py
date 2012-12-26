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

def permission_print(apps): 
    f1 = codecs.open('./txt/cm_perm_contact_only.txt', 'w', encoding='utf-8')
    f2 = codecs.open('./txt/cm_perm_contact_group.txt', 'w', encoding='utf-8')
    f3 = codecs.open('./txt/cm_perm_contact_individual.txt', 'w', encoding='utf-8')
    f1.write('app_id\tcontact_perm\t\n')
    f2.write('app_id\tperm_group\tperm_group_id\n')
    f3.write('app_id\tperm_individual\tperm_individual_id\n')
    group_ids = {}
    individual_ids = {}
    for app_id in apps:
        app = apps[app_id]
        if not app.has_key('perms'):
            continue
        perms = app['perms']
        groups = {}
        individuals = {}
        if perms.has_key('group'):
            groups = perms['group']
        if perms.has_key('individual'):
            individuals = perms['individual']
        if perms.has_key('contact_perms'):
            contact_perms = check_none(perms['contact_perms'].replace('|', '').strip(), 'none')
            if contact_perms == 'none':
                continue
            for group in groups:
                if not group_ids.has_key(group):
                    group_ids[group] = len(group_ids)+1
                group_id = group_ids[group]
                t = u'%s\t%s\t%s\t\n'%(app_id, group, group_id)
                f2.write(t)
            for individual in individuals:
                if not individual_ids.has_key(individual):
                    individual_ids[individual] = len(individual_ids)+1
                individual_id = individual_ids[individual]
                t = u'%s\t%s\t%s\t\n'%(app_id, individual, individual_id)
                f3.write(t)
    f1.close()
    f2.close()
    f3.close()
            
        
        

if __name__ == '__main__':
    apps = {}
    apps = contact_permission(apps)
    apps = app_permission(apps)
    permission_print(apps)
    
