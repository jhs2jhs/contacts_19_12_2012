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

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

price_types = ['paid', 'free']
centrality_types = ['clustering', 'degree', 'closeness', 'betweenness']

from datetime import datetime
import matplotlib.gridspec as gridspec

#######################################
def save_apps_file(apps, categories):
    fs = {}
    t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%('app_id', 'perm_id', 'rank', 'category', 'price', 'rating_average', 'rating_total', 'installs', 'developer', 'developer_website', 'developer_email', 'developer_privacy', 'youtube_has', 'youtube_view_total', 'google_plus_figure', 'award_editor', 'award_developer', 'theme_app', 'perm_counts')
    for category in categories:
        cate_id = categories[category]
        for price_type in price_types:
            if not fs.has_key(category):
                fs[category] = {}
            fs[category][price_type] = codecs.open(u'./txt_critical_perms/apps_file/%s_%s_%s.txt'%(price_type, cate_id, category), 'w', encoding='utf-8')
            fs[category][price_type].write(t)
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
        price_type = get_price_type(price)
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
        ps = {}
        perm_counts = 0
        if app.has_key('perms'):
            ps = app['perms']
            perm_counts = len(ps)
        for perm_id in ps:
            t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, perm_id, rank, category, price, rating_average, rating_total, installs, developer_href, developer_website, developer_email, developer_privacy, youtube_has, youtube_view_total, google_plus_figure, award_editor, award_developer, theme_app, perm_counts)
            fs[category][price_type].write(t)
            f.write(t)
    print '\t\tend loop'
    f.close()
    for category in categories:
        for price_type in price_types:
            fs[category][price_type].close()


def get_price_type(price):
    p = float(price)
    if p > 0:
        return 'paid'
    else:
        return 'free'


######################################
def generate_gexf_file(fp):
    print 'start to read %s.txt'%(fp)
    g = nx.Graph()
    i_t = 100000
    i_i = 0
    p = 0
    f = codecs.open('./txt_critical_perms/apps_file/%s.txt'%(fp), 'r', encoding='utf-8')
    l = f.readline()
    l = f.readline()
    while l:
        p, i_i = p_percent(p, i_i, i_t, 10)
        ls = l.split('\t')
        app_id, perm_id, rank, category, price, rating_average, rating_total, installs, developer_href, developer_website, developer_email, developer_privacy, youtube_has, youtube_view_total, google_plus_figure, award_editor, award_developer, theme_app, perm_counts, ln = ls
        g.add_node(app_id, bipartite=1, node_type='app', rank=rank, category=category, price=price, rating_average=rating_average, rating_total=rating_total, installs=installs, developer=developer_href, developer_website=developer_website, developer_email=developer_email, developer_privacy=developer_privacy, youtube_has=youtube_has, youtube_view_total=youtube_view_total, google_plus_figure=google_plus_figure, award_editor=award_editor, award_developer=award_developer, theme_app=theme_app, perm_counts=perm_counts)
        g.add_node(perm_id, bipartite=0, node_type='data')
        g.add_edge(perm_id, app_id)
        l = f.readline()
    nx.write_gexf(g, u'./txt_critical_perms/gexf/%s.gexf'%(fp))
    print 'end read %s.txt'%(fp)


def generate_gexf_file_main():
    for category in categories:
        cate_id = categories[category]
        for price_type in price_types:
            fp = u'%s_%s_%s'%(price_type, cate_id, category)
            generate_gexf_file(fp)


#######################################
def calculate_centrality(fp, centrality_type, perm_maps):
    print '%s : start to read %s.txt '%(centrality_type, fp)
    g = nx.Graph()
    i_t = 100000
    i_i = 0
    p = 0
    f = codecs.open('./txt_critical_perms/apps_file/%s.txt'%(fp), 'r', encoding='utf-8')
    l = f.readline()
    l = f.readline()
    while l:
        p, i_i = p_percent(p, i_i, i_t, 10)
        ls = l.split('\t')
        app_id = ls[0].strip().lower()
        perm_id = ls[1].strip().lower()
        g.add_node(app_id, bipartite=0) # top
        g.add_node(perm_id, bipartite=1) # buttom
        g.add_edge(app_id, perm_id)
        l = f.readline()
    is_connect = nx.is_connected(g)
    print u'end read: %s'%(fp), is_connect
    # buttom top
    #node_data, node_app = bipartite.sets(g)
    node_data = set(n for n, d in g.nodes(data=True) if d['bipartite'] == 1)
    node_app = set(g) - node_data
    ## centrality degree
    if centrality_type == 'degree':
        try:
            centrality = bipartite.degree_centrality(g, node_data)
            result = get_centrality_out(fp, node_data, node_app,  centrality, centrality_type, perm_maps)
            return result, is_connect
        except Exception as e:
            print '** error in centrality: %s : %s'%(centrality_type, fp), e 
    ## centrality closeness
    if centrality_type == 'closeness':
        try:
            centrality = bipartite.closeness_centrality(g, node_app, normalized=False)
            result = get_centrality_out(fp, node_data, node_app,  centrality, centrality_type, perm_maps)
            return result, is_connect
        except Exception as e:
            print '**** error in centrality : %s : %s'%(centrality_type, fp), e
    ## centrality betweenness
    if centrality_type == 'betweenness':
        try:
            centrality = bipartite.betweenness_centrality(g, node_app)
            result = get_centrality_out(fp, node_data, node_app,  centrality, centrality_type, perm_maps)
            return result, is_connect
        except Exception as e:
            print '**** error in centrality : %s : %s'%(centrality_type, fp), e
    if centrality_type == 'clustering':
        try:
            centrality = bipartite.clustering(g, node_data, mode='dot')
            result = get_centrality_out(fp, node_data, node_app,  centrality, centrality_type, perm_maps)
            return result, is_connect
        except Exception as e:
            print '**** error in centrality : %s : %s'%(centrality_type, fp), e
    
  
def get_centrality_out(fp, node_data, node_app, centrality, centrality_type, perm_maps):
    #print centrality
    f = codecs.open('./txt_critical_perms/centrality_category_price/%s_%s.txt'%(centrality_type, fp), 'w', encoding='utf-8')
    t = u'%s\t%s\t%s\t\n'%('node', 'centrality_score', 'data')
    f.write(t)
    for node in node_data:
        if centrality.has_key(node):
            score = centrality[node]
        else:
            score = 'none'
        if perm_maps.has_key(str(node)):
            label = perm_maps[str(node)]
        else:
            label = 'none'
        t = u'%s\t%s\t%s\t%s\t\n'%(node, score, 'perm', label)
        f.write(t)
    for node in node_app:
        if centrality.has_key(node):
            score = centrality[node]
        else:
            score = 'none'
        label = 'none'
        t = u'%s\t%s\t%s\t%s\t\n'%(node, score, 'app', label)
        f.write(t)
    f.close()
    return True
    


def get_centrality_out_main(perm_maps):
    ffs = {}
    for centrality_type in centrality_types:
        for price_type in price_types:
            for category in categories:
                cate_id = categories[category]
                cate_id = str(cate_id)
                if not ffs.has_key(cate_id):
                    ffs[cate_id] = {}
                if not ffs[cate_id].has_key(price_type):
                    ffs[cate_id][price_type] = {}
                if not ffs[cate_id][price_type].has_key(centrality_type):
                    ffs[cate_id][price_type][centrality_type] = False
    f = codecs.open('./txt_critical_perms/centrality_status.txt', 'r', encoding='utf-8')
    l = f.readline()
    while l:
        ls = l.split('\t')
        if len(ls) < 6:
            l = f.readline()
            continue
        cate_id, category, price_type, centrality_type, is_connect, ln = ls
        ffs[cate_id][price_type][centrality_type] = True
        l = f.readline()
    f.close()
    f = codecs.open('./txt_critical_perms/centrality_status.txt', 'a', encoding='utf-8')
    for centrality_type in centrality_types:
        for price_type in price_types:
            for category in categories:
                cate_id = categories[category]
                if ffs[str(cate_id)][price_type][centrality_type] == True:
                    continue
                fp = '%s_%s_%s'%(price_type, cate_id, category)
                result, is_connect = calculate_centrality(fp, centrality_type, perm_maps)
                if result == True:
                    f.write('%s\t%s\t%s\t%s\t%s\t\n'%(cate_id, category, price_type, centrality_type, is_connect))
                else:
                    print '** error in calculate_centrality method **'
                print str(datetime.now())
    f.close()


#def get_interest_centrality():

#######################################
def show_perms_centrality_plot():
    ffs = {}
    for centrality_type in centrality_types:
        for price_type in price_types:
            for category in categories:
                cate_id = categories[category]
                cate_id = str(cate_id)
                if not ffs.has_key(centrality_type):
                    ffs[centrality_type] = {}
                if not ffs[centrality_type].has_key(price_type):
                    ffs[centrality_type][price_type] = {}
                if not ffs[centrality_type][price_type].has_key(cate_id):
                    ffs[centrality_type][price_type][cate_id] = {}
    for centrality_type in centrality_types:
        for price_type in price_types:
            for category in categories:
                cate_id = categories[category]
                cate_id = str(cate_id)
                fp = '%s_%s_%s_%s'%(centrality_type, price_type, cate_id, category)
                f = codecs.open('./txt_critical_perms/centrality_category_price/%s.txt'%(fp), 'r', encoding='utf-8')
                l = f.readline()
                l = f.readline()
                while l:
                    ls = l.split('\t')
                    node_id, score, node_type, node_lable, ln = ls
                    if node_type == 'app':
                        l = f.readline()
                        continue
                    ffs[centrality_type][price_type][cate_id][node_id] = float(score)
                    l = f.readline()
            break
        break
    plt_x = len(categories)
    plt_y = len(price_types)
    plt_y = 1
    for centrality_type in centrality_types:
        j = -1
        for price_type in price_types:
            j = j + 1
            i = -1
            plt.figure('%s_%s'%(centrality_type, price_type))
            #ax_m = plt.subplot2grid((1, 1), (0, 0))
            for category in categories:
                cate_id = categories[category]
                cate_id = str(cate_id)
                i = i + 1
                #ax = plt.subplot2grid((plt_x, plt_y), (i, j))
                q = 0
                qs = []
                for perm_id in sorted(ffs[centrality_type][price_type][cate_id].iterkeys()):
                    q = q + 1
                    score = ffs[centrality_type][price_type][cate_id][perm_id]
                    #ax.plot([q, score])
                    qs.append(score)
                qs.sort()
                color = (1/(i+1), 1/(i+1), 1/(i+1))
                #plot(x, y, color='green', linestyle='dashed', marker='.', markerfacecolor='blue', markersize=12).
                plt.semilogy(qs, color=color, marker='.', label=category)
            plt.savefig('./txt_critical_perms/figs/%s_%s.pdf'%(centrality_type, price_type), format='pdf', orientation='landscape')
    
                        
    

#######################################
if __name__ == '__main__':
    op = 'save apps file'
    op = 'create gexf files'
    op = 'read apps file'
    op = 'show perm centrality plot'
    categories = category_get({})
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    p_maps = {}
    p_maps = p_map_import(p_maps)
    if op == 'save apps file':
        apps = {}
        apps = perms_fact_perms_map(perm_maps, apps)
        apps = perms_fact_awards(apps)
        apps = perms_fact_apps(apps)
        apps = cm_contacts.contact_videos(apps)
        apps = cm_contacts.contact_share(apps)
        save_apps_file(apps, categories)
    if op == 'create gexf files':
        generate_gexf_file_main()
    if op == 'read apps file':
        #print perm_maps
        get_centrality_out_main(p_maps)
        '''
        fp = 'paid_10_casual'
        fp = 'paid_22_finance'
        centrality_type = 'clustering'
        centrality_type = 'degree'
        calculate_centrality(fp, centrality_type, p_maps)
        '''
    if op == 'show perm centrality plot':
        show_perms_centrality_plot()
        
