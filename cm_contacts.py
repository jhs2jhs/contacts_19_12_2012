#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *

import sys
print sys.getdefaultencoding()
import sqlite3
import urlparse
import urllib
import codecs


print "start"
db = sqlite3.connect('db_app.db')

###############

sql_app_contact_init = '''
SELECT app_id, perm_individual FROM permission WHERE perm_individual IN ('write contact data', 'read contact data', 'read your profile data', 'write to your profile data', 'write to your social stream', 'read your social stream')
'''
sql_app_contact_init = '''
SELECT app_id, perm_individual FROM permission WHERE UPPER(perm_individual) LIKE '%CONTACT%' OR UPPER(perm_individual) LIKE '%PROFILE%' OR UPPER(perm_individual) LIKE '%SOCIAL%'
'''
sql_app_contact_insert = '''
INSERT OR IGNORE INTO app_contact (app_id, perm) VALUES (?,?)
'''
def app_contact_init():
    apps = {}
    c = db.cursor()
    c.execute(sql_app_contact_init, ())
    print 'contact init start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        perm = r[1].strip().encode('utf-8').strip().lower()
        if apps.has_key(app_id):
            if apps[app_id].has_key('permission'):
                if apps[app_id]['permission'].has_key(perm):
                    apps[app_id]['permission'][perm] = apps[app_id]['permission'][perm] + 1
                else:
                    apps[app_id]['permission'][perm] = 0
            else:
                apps[app_id]['permission'] = {perm:0}
        else:
            apps[app_id] = {'permission':{perm:0}}
        r = c.fetchone()
    c.close()
    print "apps total:", len(apps)
    c = db.cursor()
    for app_id in apps:
        app = apps[app_id]
        perms = app['permission']
        perm_t = ''
        for perm in perms:
            perm_c = perms[perm]
            if perm_c > 1:
                print "error perm_c > 1", perm_c
            t = ''
            perm = perm.lower()
            t = 'ot'
            if perm == 'write contact data':
                t = 'cw'
            if perm == 'read contact data':
                t = 'cr'
            if perm == 'read your profile data':
                t = 'pr'
            if perm == 'write to your profile data':
                t = 'pw'
            if perm == 'write to your social stream':
                t = 'sw'
            if perm == 'read your social stream':
                t = 'sr'
            if t == '':
                print "error t == "
            perm_t = '%s|%s'%(perm_t, t)
        if 'c' in perm_t or 'p' in perm_t or 's' in perm_t or 'o' in perm_t:
            c.execute(sql_app_contact_insert, (app_id, perm_t))
    db.commit()
    c.close()
    print 'contact init end'
    print len(apps)


sql_contact_permission_get = '''
SELECT app_contact.app_id, app_contact.perm FROM app_contact
'''
def contact_permission(apps):
    c = db.cursor()
    c.execute(sql_contact_permission_get, ())
    print 'contact_permission start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').strip().lower()
        perms = r[1]
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('contact_perms'):
            apps[app_id]['perms'] = {}
        apps[app_id]['perms']['contact_perms'] = perms
        r = c.fetchone()
    c.close()
    print 'contact_permission end', len(apps)
    return apps

sql_app_permission_get = '''
SELECT permission.app_id, permission.perm_group, permission.perm_individual FROM permission
'''
def app_permission(apps):
    c = db.cursor()
    c.execute(sql_app_permission_get, ())
    print 'app_permission start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').strip().lower()
        group = r[1].encode('utf-8').strip().lower()
        individual = r[2].encode('utf-8').strip().lower()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('perms'):
            apps[app_id]['perms'] = {}
        if not apps[app_id]['perms'].has_key('group'):
            apps[app_id]['perms']['group'] = {}
        apps[app_id]['perms']['group'][group] = 1
        if not apps[app_id]['perms'].has_key('individual'):
            apps[app_id]['perms']['individual'] = {}
        apps[app_id]['perms']['individual'][individual] = 1
        r = c.fetchone()
    c.close()
    print 'app_permission end', len(apps)
    return apps

sql_contact_videos = '''
SELECT videos.app_id, videos.video, videos.view_total, videos.view_likes, videos.view_dislikes, videos.comments FROM videos
'''
def contact_videos(apps):
    c = db.cursor()
    c.execute(sql_contact_videos, ())
    print 'contact_videos start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').strip().lower()
        video = r[1].encode('utf-8').strip() ######## lower()?
        if video == '':
            continue
        view_total = r[2].replace(',','').strip()
        view_likes = r[3].replace(',','').strip()
        view_dislikes = r[4].replace(',','').strip()
        comments = r[5].replace(',','').strip()
        if video.strip() == '':
            continue
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('youtube'):
            apps[app_id]['youtube'] = {}
        apps[app_id]['youtube']['video'] = video
        apps[app_id]['youtube']['view_total'] = view_total
        apps[app_id]['youtube']['view_likes'] = view_likes
        apps[app_id]['youtube']['view_dislikes'] = view_dislikes
        apps[app_id]['youtube']['comments'] = comments
        r = c.fetchone()
    c.close()
    print 'leave videos', len(apps)
    return apps

sql_contact_awards = '''
SELECT awards.app_id, awards.award FROM awards
'''
def contact_awards(apps):
    c = db.cursor()
    c.execute(sql_contact_awards, ())
    print 'contact_awards start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').strip().lower()
        award = r[1].encode('utf-8').strip().lower()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('awards'):
            apps[app_id]['awards'] = {}
        apps[app_id]['awards'][award] = 1
        r = c.fetchone()
    c.close()
    print 'leave award', len(apps)
    return apps

sql_contact_share = '''
SELECT share.app_id, share.google_plus_figure FROM share
'''
def contact_share(apps):
    c = db.cursor()
    c.execute(sql_contact_share, ())
    print 'contact_share start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').strip().lower()
        google_plus_figure = r[1].encode('utf-8').strip().lower() ## they have .k to process
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('share'):
            apps[app_id]['share'] = {}
        apps[app_id]['share']['google_plus'] = google_plus_figure
        r = c.fetchone()
    c.close()
    print 'leave share', len(apps)
    return apps

## screenshot is not available 

# missing: update_date, current_version
sql_contact_app = '''
SELECT app.app_id, 
app.developer_href, app.developer_website, app.developer_email, app.developer_privacy,
app.desc, 
app.category,
app.installs,
app.price,
app.content_rating,
app.rating_total,
app.rating_average,
app.rating_0,
app.rating_1,
app.rating_2,
app.rating_3,
app.rating_4,
app.rating_5,
title,
developer_name,
requires_android,
file_size, 
rank,
update_date 
FROM app 
WHERE developer_href IS NOT NULL
'''
def contact_app(apps):
    c = db.cursor()
    c.execute(sql_contact_app, ())
    print 'contact_app start'
    r = c.fetchone()
    while r != None:
        app_id = r[0].encode('utf-8').lower().strip()
        developer_href = r[1].strip()
        #developer_href = get_url_query(developer_href, 'id')
        developer_website = r[2].strip()
        #developer_website = get_url_query(developer_website, 'q')
        developer_email = r[3].encode('utf-8').strip()
        developer_privacy = r[4].strip()
        #developer_privacy = get_url_query(developer_privacy, 'q')
        desc = r[5].strip()
        desc_len = len(desc)
        category = r[6].encode('utf-8').strip().lower()
        installs = r[7].replace(',','').encode('utf-8').strip()
        price = r[8].strip().encode('utf-8').lower()
        if price == 'install':
            price = '0'
        else:
            if '$' in price:
                prices = price.split('$')
                print price, prices
            if '£' in price:
                prices = price.split('£')
            price = prices[1]
        # not use : content_rating = r[9].encode('utf-8').strip()
        rating_total = r[10].replace(',', '').encode('utf-8').strip()
        rating_average = r[11].strip()
        #rating_0 = r[12].replace(',', '').encode('utf-8').strip()
        rating_1 = r[13].replace(',', '').encode('utf-8').strip()
        rating_2 = r[14].replace(',', '').encode('utf-8').strip()
        rating_3 = r[15].replace(',', '').encode('utf-8').strip()
        rating_4 = r[16].replace(',', '').encode('utf-8').strip()
        rating_5 = r[17].replace(',', '').encode('utf-8').strip()
        title = r[18].encode('utf-8', 'replace').strip()
        developer_name = r[19].encode('utf-8', 'replace').strip()
        required_android = r[20].encode('utf-8').strip()
        file_size = r[21].encode('utf-8').strip().lower()
        rank = r[22].encode('utf-8').strip()
        update_date = r[23].encode('utf-8').strip()
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('developers'):
            apps[app_id]['developers'] = {}
        apps[app_id]['developers']['developer_href'] = developer_href
        apps[app_id]['developers']['developer_website'] = developer_website
        apps[app_id]['developers']['developer_email'] = developer_email
        apps[app_id]['developers']['developer_privacy'] = developer_privacy
        apps[app_id]['developers']['developer_name'] = developer_name
        # not use: apps[app_id]['content_rating'] = content_rating
        ###
        apps[app_id]['rating_total'] = rating_total
        apps[app_id]['rating_average'] = rating_average
        #apps[app_id]['ratings']['rating_0'] = rating_0
        apps[app_id]['rating_1'] = rating_1
        apps[app_id]['rating_2'] = rating_2
        apps[app_id]['rating_3'] = rating_3
        apps[app_id]['rating_4'] = rating_4
        apps[app_id]['rating_5'] = rating_5
        ###
        apps[app_id]['installs'] = installs
        apps[app_id]['desc_len'] = desc_len
        apps[app_id]['category'] = category
        apps[app_id]['price'] = price
        apps[app_id]['app_title'] = title
        apps[app_id]['required_android'] = required_android
        apps[app_id]['file_size'] = file_size
        apps[app_id]['app_rank'] = rank
        apps[app_id]['update_date'] = update_date
        r = c.fetchone()
    c.close()
    print 'contact_app end', len(apps)
    return apps

def contact_apps_print(apps):
    print "contact apps print start"
    f = codecs.open('./txt/cm_contact_apps.txt', 'w', encoding='utf-8')
    f.write('%s\t%s\t%s\t%s\t'%('app_id', 'category', 'category_id', 'price'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('rating_average', 'rating_total', 'update_date', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5'))
    f.write('%s\t%s\t%s\t%s\t%s\t'%('contact_has', 'contact_perms', 'contact_perms_type', 'perm_groups', 'perm_individuals'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('developer_href', 'developer_id', 'developer_website', 'developer_email', 'developer_privacy', 'developer_name'))
    f.write('%s\t%s\t%s\t%s\t'%('installs', 'install_min', 'install_max', 'install_average'))
    f.write('%s\t%s\t%s\t%s\t%s\t'%('youtube_has', 'view_total', 'view_likes', 'view_dislikes', 'view_comments'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('google_plus_figure', 'awards_len', 'desc_len', 'app_title', 'required_android', 'file_size', 'rank', 'rank_has'))
    f.write('\n')
    developers = {}
    categories = {}
    for app_id in apps:
        app = apps[app_id]
        if app.has_key('developers'):
            developer = app['developers']
            developer_href = check_none(developer['developer_href'], 'none')
            if developer_href == 'none':
                print "small mistake, developer_href == none"
                continue
            if not developers.has_key(developer_href):
               developers[developer_href] = len(developers)+1
            developer_id = unicode(developers[developer_href])
            developer_website = check_none(developer['developer_website'], 'none')
            developer_email = check_none(developer['developer_email'], 'none')
            developer_privacy = check_none(developer['developer_privacy'], 'none')
            developer_name = check_none(developer['developer_name'], 'none')
        else:
            #print "big mistake: developer is not exist"
            continue
            #developer_id = 'none'
            #developer_href = 'none'
            #developer_website = 'none'
            #developer_email = 'none'
            #developer_privacy = 'none'
            #developer_name = 'none'
        ### rating
        rating_total = check_none(app['rating_total'], 'none')
        #if rating_total == 'none':
        #    print "small mistake, rating_total == none"
        #    continue
        #if int(rating_total) < 5:
        #    print 'for bias'
        #    continue 
        rating_average = check_none(app['rating_average'], 'none')
        #if rating_average == 'none':
        #    print "small mistake, rating_average == none"
        #    continue
        rating_1 = check_none(app['rating_1'], '0')
        rating_2 = check_none(app['rating_2'], '0')
        rating_3 = check_none(app['rating_3'], '0')
        rating_4 = check_none(app['rating_4'], '0')
        rating_5 = check_none(app['rating_5'], '0')
        update_date = check_none(app['update_date'], 'none')
        ### installs
        installs = check_none(app['installs'], '0')
        if '-' not in installs:
            #print installs, 0, 0
            install_min = 0
            install_max = 0
            installs = '0 - 0'
            install_average = '0'
        else:
            install = installs.split('-')
            install_min = install[0].replace(',', '').strip()
            install_max = install[1].replace(',', '').strip()
            install_average = str((int(install_min) + int(install_max))/2)
            install_min = check_none(install_min, '0')
            install_max = check_none(install_max, '0')
        ### 
        if app.has_key('share'):
            google_plus_figure = check_none(app['share']['google_plus'], '0')
            google_plus_figure = figures(google_plus_figure, 'k', 1000)
        else:
            google_plus_figure = 'none'
        if app.has_key('awards'):
            awards_len = len(app['awards'])
        else:
            awards_len = '0'
        if app.has_key('youtube'):
            youtube = app['youtube']
            view_total = check_none(youtube['view_total'], '0')
            view_likes = check_none(youtube['view_likes'], '0')
            view_dislikes = check_none(youtube['view_dislikes'], '0')
            view_comments = check_none(youtube['comments'], '0')
            youtube_has = '1'
        else:
            view_total = 'none'
            view_likes = 'none'
            view_dislikes = 'none'
            view_comments = 'none'
            youtube_has = '0'
        if app.has_key('perms'):
            perms = app['perms']
            if perms.has_key('contact_perms'):
                contact_perms = perms['contact_perms'] ## needs to know the type
                contact_perms_type, contact_has = contact_level(contact_perms)
                contact_has = '1'
            else:
                contact_perms = 'none'
                contact_has = '0'
                contact_perms_type = '0'
            if perms.has_key('group'):
                perm_groups = len(perms['group'])
            else:
                perm_groups = '0'
            if perms.has_key('individual'):
                perm_individuals = len(perms['individual'])
            else:
                perm_individuals = '0'
        else:
            contact_perms = 'none'
            contact_has = '0'
            perm_groups = '0'
            perm_individuals = '0'
        desc_len = check_none(app['desc_len'], '0')
        category = check_none(app['category'], 'none')
        if not categories.has_key(category):
            categories[category] = len(categories)+1
        category_id = unicode(categories[category])
        price = check_none(app['price'], '0')
        app_title = check_none(app['app_title'], 'none')
        required_android = check_none(app['required_android'], 'none')
        file_size = check_none(app['file_size'], '0')
        file_size = figures(file_size, 'k', 1024)
        file_size = figures(file_size, 'm', 1048576) # 1024*1024
        rank = check_none(app['app_rank'], 'none')
        if rank == '-1' or rank == '0':
            rank = 'none'
            rank_has = '0'
        else:
            rank_has = '1'
        ## yes or no
        developer_website = yes_no(developer_website)
        developer_email = yes_no(developer_email)
        developer_privacy = yes_no(developer_privacy)
        t = u""
        t = u'%s\t%s\t%s\t%s\t'%(app_id, category, category_id, price)
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(t, rating_average, rating_total, update_date, rating_1, rating_2, rating_3, rating_4, rating_5)
        t = u'%s%s\t%s\t%s\t%s\t%s\t'%(t, contact_has, contact_perms, contact_perms_type, perm_groups, perm_individuals)
        t = u"%s%s\t%s\t%s\t%s\t%s\t%s\t"%(t, developer_href, developer_id, developer_website, developer_email, developer_privacy, developer_name)
        t = u'%s%s\t%s\t%s\t%s\t'%(t, installs, install_min, install_max, install_average)
        t = u'%s%s\t%s\t%s\t%s\t%s\t'%(t, youtube_has, view_total, view_likes, view_dislikes, view_comments)
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(t, google_plus_figure, awards_len, desc_len, app_title, required_android, file_size, rank, rank_has)
        t = u'%s\n'%t
        f.write(t)
    f.close()
    f1 = codecs.open('./txt/cm_contact_category.txt', 'w', encoding='utf-8')
    f1.write('category_id\tcategory\n')
    for category in categories:
        category_id = unicode(categories[category])
        f1.write(u'%s\t%s\n'%(category_id, category))
    f1.close()
    print "contact_app_print end"
        


if __name__ == "__main__":
    app_contact_init()
    apps = {}
    apps = contact_permission(apps)
    apps = app_permission(apps)
    apps = contact_videos(apps)
    apps = contact_awards(apps)
    apps = contact_share(apps)
    apps = contact_app(apps)
    contact_apps_print(apps)
    #return 
