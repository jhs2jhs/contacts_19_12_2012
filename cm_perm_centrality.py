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
import cm_user_data

print "start"
db = sqlite3.connect('db_app.db')

#######################################


# http://networkx.lanl.gov/archive/networkx-1.5/reference/generated/networkx.algorithms.bipartite.centrality.degree_centrality.html#networkx.algorithms.bipartite.centrality.degree_centrality
# http://networkx.lanl.gov/archive/networkx-1.5/reference/algorithms.bipartite.html
# http://networkx.github.com/documentation/latest/reference/algorithms.bipartite.html

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
'''
B = nx.Graph()
B.add_nodes_from([1,2,3,4], bipartite=0) # Add the node attribute "bipartite"
B.add_nodes_from(['a','b','c'], bipartite=1)
B.add_edges_from([(1,'a'), (1,'b'), (2,'b'), (2,'c'), (3,'c'), (4,'a')])
t, b = bipartite.sets(B)
print t, b
print bipartite.centrality.degree_centrality(B, b)
print bipartite.degree_centrality(B, t)
print ''
m = bipartite.projected_graph(B, t)
#nx.draw(m)
l = bipartite.projected_graph(B, b)
#nx.draw(l)
#plt.show()
print m.edges()
#m = bipartite.projected_graph(B, b)
#print m.edges()
print bipartite.clustering(B, t)
print nx.nodes(B)
B.add_edge(1, 2)
B.add_edge(2, 3, weight=0.9)
print nx.nodes(B)
print nx.get_node_attributes(B, 'weight')
print nx.get_node_attributes(B, 'bipartite')
nx.write_gexf(B, './txt_user_data/test.gexf')

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3, weight=0.9)
G.add_node(1, bipartite=0)
G.add_node(5, bipariite=3)
G.add_node(5, b=3)
G.add_node(3, bipartite=1)
print nx.nodes(G)
print nx.get_node_attributes(G, 'bipartite')
print nx.get_node_attributes(G, 'b')
#nx.draw(G)
#nx.write_gexf(G, './txt_user_data/test1.gexf')
#plt.show()
'''

def get_node_data(g, user_data_types):
    for data_group in user_data_types:
        for data_type in user_data_types[data_group]:
            g.add_node(data_type, bipartite=1, node_type='data')
            #print data_type
    return g

def save_apps_file(apps, categories, user_data_types, user_data_map):
    fs = {}
    t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%('app_id', 'data_type', 'edge_weight', 'rank', 'category', 'price', 'rating_average', 'rating_total', 'installs', 'developer', 'developer_website', 'developer_email', 'developer_privacy', 'youtube_has', 'youtube_view_total', 'google_plus_figure', 'award_editor', 'award_developer', 'theme_app', 'perm_counts')
    for category in categories:
        cate_id = categories[category]
        fs[category] = codecs.open(u'./txt_user_data/apps_file/%s_%s.txt'%(cate_id, category), 'w', encoding='utf-8')
        fs[category].write(t)
    f = codecs.open(u'./txt_user_data/apps_file/all.txt', 'w', encoding='utf-8')
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
        developer_website = app['developer_website']
        developer_email = app['developer_email']
        developer_privacy = app['developer_privacy']
        rank = -2
        if app.has_key('rank'):
            rank = app['rank']
        if app.has_key('youtube'):
            youtube_has = '1'
            youtube_view_total = check_none(app['youtube']['view_total'], '0')
        else:
            youtube_has = '0'
            youtube_view_total = 'none'
        if app.has_key('share'):
            google_plus_figure = check_none(app['share']['google_plus'], '0')
        else:
            google_plus_figure = 'none'
        award_editor = '0'
        award_developer = '0'
        if app.has_key('awards'):
            for award in app['awards']:
                award = award.strip().lower()
                if award == 'top developer':
                    award_developer = '1'
                if award == "editors' choice":
                    award_editor = '1'
        theme_app = app['theme_app']
        if not app.has_key('perms'):
            ps = {}
            perm_counts = 0
        else: 
            ps = app['perms']
            perm_counts = len(ps)
            #print ps
        for data_group in user_data_types:
            for data_type in user_data_types[data_group]:
                p_id_c_t = 0
                for p_opt in user_data_types[data_group][data_type]:
                    #p_id_c = 0
                    for p_id in user_data_types[data_group][data_type][p_opt]:
                        if ps.has_key(p_id):
                            #p_id_c = p_id_c + 1
                            p_id_c_t = p_id_c_t + 1
                    #t = u'%s%s\t'%(t, p_id_c)
                if p_id_c_t > 0:
                    weight = get_edge_weight(data_type)
                    '''# those two category are empty 
                    if category == 'arcade & action' or categry == 'cards & casino':
                        print category, weight
                    '''
                    if weight > 1:
                        edge_weight = float(p_id_c_t)/weight 
                        t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, data_type, edge_weight, rank, category, price, rating_average, rating_total, installs, developer_href, developer_website, developer_email, developer_privacy, youtube_has, youtube_view_total, google_plus_figure, award_editor, award_developer, theme_app, perm_counts)
                        fs[category].write(t)
                        f.write(t)
    print '\t\tend loop'
    f.close()
    for category in categories:
        fs[category].close()
        

def get_edge_weight(data_type):
    divs = {
        'control':44,
        'connection_media':6,
        'network behavior':8,
        'app behavior':13,
        'device behavior':19,
        'account info':10,
        'contact info':6,
        'locaton info':4,
        'message info':19,
        'storage':7,
        'history':7,
        }
    if divs.has_key(data_type):
        return divs[data_type]
    else:
        print u'error in get_edge_weight %'%(data_type)
        return 1


##########################################
def read_apps_file(fp, ot, user_data_types, ffs, centrality_type):
    print 'start to read %s.txt'%(fp)
    g = nx.Graph()
    i_t = 100000
    i_i = 0
    p = 0
    f = codecs.open('./txt_user_data/apps_file/%s.txt'%(fp), 'r', encoding='utf-8')
    l = f.readline()
    l = f.readline()
    while l:
        p, i_i = p_percent(p, i_i, i_t, 10)
        ls = l.split('\t')
        app_id, data_type, edge_weight, rank, category, price, rating_average, rating_total, installs, developer_href, developer_website, developer_email, developer_privacy, youtube_has, youtube_view_total, google_plus_figure, award_editor, award_developer, theme_app, perm_counts, ln = ls
        g.add_node(app_id, bipartite=1, node_type='app', rank=rank, category=category, price=price, rating_average=rating_average, rating_total=rating_total, installs=installs, developer=developer_href, developer_website=developer_website, developer_email=developer_email, developer_privacy=developer_privacy, youtube_has=youtube_has, youtube_view_total=youtube_view_total, google_plus_figure=google_plus_figure, award_editor=award_editor, award_developer=award_developer, theme_app=theme_app, perm_counts=perm_counts)
        g.add_node(data_type, bipartite=0, node_type='data')
        g.add_edge(data_type, app_id, weight=edge_weight)
        l = f.readline()
        #if i_i > 10000:
        #    break
    print u'end read: %s'%(fp)
    node_data, node_app = bipartite.sets(g)
    #print node_data
    #print node_app
    #nx.write_gexf(g, u'./txt_user_data/gexf/%s.gexf'%(fp))
    print u'write to file'
    f = codecs.open('./txt_user_data/centrality/%s.txt'%(centrality_type), 'a', encoding='utf-8')
    if len(ffs[centrality_type]) == 0:
        t = u'cate_id\tcategory\tcentrality_type\t'
        for data_group in user_data_types:
            for data_type in user_data_types[data_group]:
                t = u'%s%s\t'%(t, data_type)
        t = u'%s\n'%(t)
        f.write(t)
    #print node_data
    #m = bipartite.projected_graph(g, node_app)
    #print m.edges()
    ## centrality degree
    if centrality_type == 'degree':
        print centrality_type, cate_id, ffs[centrality_type]
        try:
            centrality = bipartite.centrality.degree_centrality(g, node_app)
            print 'centrality calculated: %s'%(centrality_type)
            t = u'%s%s\t'%(ot, centrality_type)
            t = get_centrality_out(t, user_data_types, centrality)
            f.write(u'%s\n'%(t))
        except:
            centrality = {}
            print '**** error in centrality calculation: %s : %s'%(centrality_type, fp) 
    ## centrality closeness
    if centrality_type == 'closeness':
        print centrality_type, cate_id, ffs[centrality_type]
        try:
            centrality = bipartite.centrality.closeness_centrality(g, node_app, normalized=False)
            print 'centrality calculated: %s'%(centrality_type)
            t = u'%s%s\t'%(ot, centrality_type)
            t = get_centrality_out(t, user_data_types, centrality)
            f.write(u'%s\n'%(t))
        except:
            centrality = {}
            print '**** error in centrality calculation: %s : %s'%(centrality_type, fp)
    ## centrality betweenness
    if centrality_type == 'betweenness':
        print centrality_type, cate_id, ffs[centrality_type]
        try:
            centrality = bipartite.centrality.betweenness_centrality(g, node_app)
            print 'centrality calculated: %s'%(centrality_type)
            t = u'%s%s\t'%(ot, centrality_type)
            t = get_centrality_out(t, user_data_types, centrality)
            f.write(u'%s\n'%(t))
        except:
            centrality = {}
            print '**** error in centrality calculation: %s : %s'%(centrality_type, fp)
    ## print to file
    print 'read_file_app end'


#def get_centrality(g, nodes, centrality_type, t, user_data_types, centrality):
    

def get_centrality_out(t, user_data_types, centrality):
    i = 0
    for data_group in user_data_types:
        for data_type in user_data_types[data_group]:
            if centrality.has_key(data_type):
                score = centrality[data_type]
            else:
                score = 'none'
            t = u'%s%s\t'%(t, score)
            print i, 
            i = i + 1
    return t
  


#######################################
if __name__ == '__main__':
    op = 'save apps file'
    op = 'read apps file'
    categories = category_get({})
    user_data_map = {}
    user_data_types = {}
    user_data_map, user_data_types = cm_user_data.user_data_import(user_data_map, user_data_types)
    if op == 'save apps file':
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
        save_apps_file(apps, categories, user_data_types, user_data_map)
    if op == 'read apps file':
        centrality_types = ['closeness', 'degree', 'betweenness']
        print 'read existing file start'
        ffs = {}
        for centrality_type in centrality_types:
            try:
                f = codecs.open('./txt_user_data/centrality/%s.txt'%(centrality_type), 'r', encoding='utf-8')
                if not ffs.has_key(centrality_type):
                    ffs[centrality_type] = []
                l = f.readline()
                l = f.readline()
                while l:
                    ls = l.split('\t')
                    cate_id = ls[0].strip()
                    if cate_id == '':
                        l = f.readline()
                        continue
                    if len(ls) > 3:
                        score = ls[3].strip().lower()
                        if score == 'none':
                            l = f.readline()
                            continue
                    ffs[centrality_type].append(cate_id)
                    l = f.readline()
                f.close()
            except:
               ffs[centrality_type] = [] 
            print ffs[centrality_type]
        print 'read existing file done'
        # for all 
        #fp = u'all'
        #read_apps_file(fp)
        # for each category
        for centrality_type in centrality_types:
            i = 1
            for category in categories:
                cate_id = categories[category]
                if unicode(cate_id) in ffs[centrality_type]:
                    print "== read done: ", centrality_type, cate_id, category
                    continue
                fp = u'%s_%s'%(cate_id, category)
                ot = u'%s\t%s\t'%(cate_id, category)
                read_apps_file(fp, ot, user_data_types, ffs, centrality_type)
                print u'**** (%s) %s %s end ***'%(i, cate_id, category)
                i = i + 1
        #for centrality_type in centrality_types:
        #    fs[centrality_type].close()
            
    
