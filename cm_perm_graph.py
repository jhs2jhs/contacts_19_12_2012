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
from gexf import Gexf

def perm_to_app_cate(apps, apps_t):
    print "perm_to_app_cate start"
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
        installs = app['installs']
        installs, install_min, install_max, install_average = installs_c(installs)
        if int(install_max) <= 5:
            continue
        rating_average = app['rating_average']
        if float(rating_average) == 0:
            continue
        category = app['category'].lower().strip()
        if not apps_t.has_key(category):
            apps_t[category] = {}
        apps_t[category][app_id] = app
    print "perm_to_app_Cate end"
    return apps_t


def perm_to_app_graph_each(apps_t, p_maps, categories):
    for category in apps_t:
        print 'perm_to_app_graph start ', category
        category_id = categories[category]
        apps = apps_t[category]
        gexf = Gexf('Jianhua Shao', category)
        graph = gexf.addGraph('directed', 'static', category)
        attr_node = graph.addNodeAttribute('node_type', 'app', 'string')
        attr_edge = graph.addEdgeAttribute('edge_type', 'no', 'string')
        #attr_node_app_award = graph.addNodeAttribute('app_award', 'no', 'string')
        for p_id in p_maps:
            p_label = p_maps[p_id]
            n = graph.addNode(p_id, '%s_%s'%(str(p_id), p_label))
            n.addAttribute(attr_node, 'p')
        app_ids = {}
        for app_id in apps:
            app = apps[app_id]
            award_editor = 'no'
            award_developer = 'no'
            if app.has_key('awards'):
                for award in app['awards']:
                    award = award.strip().lower()
                    if award == 'top developer':
                        award_developer = 'yes'
                    if award == "editors' choice":
                        award_editor = 'yes'
            if not app_ids.has_key(app_id):
                app_ids[app_id] = 1
                n = graph.addNode(app_id, app_id)
                n.addAttribute(attr_node, 'a')
            ps = app['perms']
            for p_id in ps:
                e = graph.addEdge('%s_%s'%(str(p_id), app_id), p_id, app_id)
                e.addAttribute(attr_edge, award_editor)
        output_file = open('./txt/graph/%s_%s.gexf'%(str(category_id), category), 'w')
        gexf.write(output_file)
        print 'perm_to_app_graph end ', category


def perm_to_app_graph_all(apps, p_maps, categories):
    print 'perm_to_app_graph start ', 'all'
    gexf_a = Gexf('Jianhua Shao', 'all')
    graph_a = gexf_a.addGraph('directed', 'static', 'all')
    attr_node_a = graph_a.addNodeAttribute('node_type', 'app', 'string')
    attr_edge_a = graph_a.addEdgeAttribute('edge_type', 'no', 'string')
    for p_id in p_maps:
        p_label = p_maps[p_id]
        n_a = graph_a.addNode(p_id, '%s_%s'%(str(p_id), p_label))
        n_a.addAttribute(attr_node_a, 'p')
    app_ids_a = {}
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
        installs = app['installs']
        installs, install_min, install_max, install_average = installs_c(installs)
        if int(install_max) <= 5:
            continue
        rating_average = app['rating_average']
        if float(rating_average) == 0:
            continue
        category = app['category'].lower().strip()
        category_id = categories[category]
        award_editor = 'no'
        award_developer = 'no'
        if app.has_key('awards'):
            for award in app['awards']:
                award = award.strip().lower()
                if award == 'top developer':
                    award_developer = 'yes'
                if award == "editors' choice":
                    award_editor = 'yes'
        if not app_ids_a.has_key(app_id):
            app_ids_a[app_id] = 1
            n_a = graph_a.addNode(app_id, app_id)
            n_a.addAttribute(attr_node_a, 'a')
        ps = app['perms']
        for p_id in ps:
            e_a = graph_a.addEdge('%s_%s'%(str(p_id), app_id), p_id, app_id)
            e_a.addAttribute(attr_edge_a, award_editor)
    output_file_a = open('./txt/graph/all.gexf', 'w')
    gexf_a.write(output_file_a)
    print 'perm_to_app_graph end all '
            


########################## sequence analysis
def gen_seq(apps, p_maps):
    gens = {}
    print 'START == '
    for p_id in p_maps:
        print p_id, 
    print ' == END'
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
        installs = app['installs']
        installs, install_min, install_max, install_average = installs_c(installs)
        if int(install_max) <= 5:
            continue
        rating_average = app['rating_average']
        if float(rating_average) == 0:
            continue
        if not app.has_key('awards'):
            continue
        award_developer = 'no'
        for award in app['awards']:
            award = award.strip().lower()
            if award == 'top developer':
                award_developer = 'yes'
        if award_developer == 'no':
            continue
        category = app['category']
        if not category.strip().lower() == 'social':
            continue
        ps = app['perms']
        seq = ''
        for p_id in p_maps:
            flag = 'N'
            if ps.has_key(p_id):
                flag = 'Y'
            seq = '%s%s'%(seq, flag)
        if not gens.has_key(seq):
            gens[seq] = {}
        if not gens[seq].has_key(category):
            gens[seq][category] = 0
        gens[seq][category] = 1 + gens[seq][category]
    print len(gens)
    #f = codecs.open('./txt/cm_perm_sequence.txt', 'w', encoding='utf-8')
    #f = codecs.open('./txt/cm_perm_sequence.phylib', 'w', encoding='utf-8')
    f = codecs.open('./txt/cm_perm_sequence_27_social.fasta', 'w', encoding='utf-8')
    #t = u's_id\tsequence\tcategories\tapps\n'
    #t = u'   %s   %s \n'%(len(gens), len(p_maps))
    #f.write(t)
    i = 0
    for seq in gens:
        i = i + 1
        seq_id = '%.10d'%i
        category_total = len(gens[seq])
        apps_total = 0
        for category in gens[seq]:
            apps_count = gens[seq][category]
            apps_total = apps_total + apps_count
        #t = u'%s\t%s\t%s\t%s\n'%(seq_id, seq, category_total, apps_total)
        #t = u'%s%s\n'%(seq_id, seq)
        t = u'>s_%s\n%s\n'%(seq_id, seq)
        f.write(t)
        print seq_id, apps_total
    f.close()
    print len(gens)

##########################

if __name__ == '__main__':
    p_maps = {}
    p_maps = p_map_import(p_maps)
    perm_maps = {}
    perm_maps = perm_map_import(perm_maps)
    apps = {}
    apps = perms_fact_perms_map(perm_maps, apps)
    apps = perms_fact_awards(apps)
    apps = perms_fact_apps(apps)
    gen_seq(apps, p_maps)
    #categories = category_get({})
    #perm_to_app_graph_all(apps, p_maps, categories)
    #apps_t = {}
    #apps_t = perm_to_app_cate(apps, apps_t)
    #perm_to_app_graph_each(apps_t, p_maps, categories)

