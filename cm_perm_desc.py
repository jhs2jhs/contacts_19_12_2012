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

################################

sql_perm_group = '''
SELECT perm_group, perm_individual FROM permission ORDER BY perm_group
'''
def perm_group ():
    print 'perm_group start'
    perms = {}
    f = open('./txt/perm_group.txt', 'w')
    f.write('%s\t%s\t%s\n'%('perm_group', 'perm_individual', 'request_count'))
    c = db.cursor()
    c.execute(sql_perm_group, ())
    r = c.fetchone()
    while r != None:
        perm_group = r[0]
        perm_individual = r[1]
        if not perms.has_key(perm_group):
            perms[perm_group] = {}
        if not perms[perm_group].has_key(perm_individual):
            perms[perm_group][perm_individual] = 0
        perms[perm_group][perm_individual] = perms[perm_group][perm_individual] + 1
        r = c.fetchone()
    for perm_group in perms:
        for perm_individual in perms[perm_group]:
            request_count = perms[perm_group][perm_individual]
            print perm_group, perm_individual, request_count
            f.write('%s\t%s\t%s\n'%(perm_group, perm_individual, request_count))
    f.close()
    c.close()
    print 'perm_group end'


if __name__ == '__main__':
    perm_group()
