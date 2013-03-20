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
import networkx as nx
import matplotlib.pyplot as plt

print "start"
db = sqlite3.connect('db_app.db')

########################################
g = nx.Graph()
g.add_node(1)
g.add_nodes_from([2,3])
h = nx.path_graph(10)
g.add_nodes_from(h)
g.add_edge(1,2)
g.add_edges_from([(1,2), (1,3)])
g.add_node('spam')
g.add_edge(1, 2, color='red')
g.add_edge(1, 2, color='red')
nx.draw_networkx_nodes(g, nx.spring_layout(g), nodelist=[1,2,5,6], node_shape='s')
nx.draw_networkx_edges(g, nx.spring_layout(g))
plt.show()
    
            
########################################
if __name__ == '__main__':
    '''
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
    '''
