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
def developers_apps(apps, developers):
    print 'developers_apps start'
    for app_id in apps:
        app = apps[app_id]
        if not app.has_key('developers'):
            continue
        #rating_total = check_none(app['rating_total'], 'none')
        #if rating_total == 'none':
        #    continue
        #rating_average = check_none(app['rating_average'], 'none')
        #if rating_average == 'none':
        #    continue
        developer = app['developers']
        developer_href = check_none(developer['developer_href'], 'none')
        if not developers.has_key(developer_href):
            developers[developer_href] = {}
        developers[developer_href][app_id] = app
        #del app
    del apps
    print 'developer_apps end ', len(developers)
    return developers


'''
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('dev_href', 'apps_len', 'apps_r_average', 'contact_has', 'category_len', 'privacy_has'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('contact_apps_rating_average', 'contact_apps_rating_average', 'contact_apps_rating', 'contact_apps_rating_no', 'contact_apps', 'contact_apps_no', 'contact_apps_category_len', 'contact_apps_category_no'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('privacy_apps', 'privacy_apps_no', 'privacy_apps_rating', 'privacy_apps_rating_no', 'privacy_apps_rating_average', 'privacy_apps_rating_no_average'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('video_apps_rating', 'video_apps_rating_no', 'video_apps', 'video_apps_no', 'video_apps_rating_average', 'video_apps_rating_no_average', 'video_apps_rating_average', 'video_apps_rating_no_average'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('website_apps_rating', 'website_apps_rating_no', 'website_apps', 'website_apps_no', 'website_apps_rating_average', 'website_apps_rating_no_average'))
'''

def developers_apps_print(developers):
    print 'developer_apps_print start'
    f = codecs.open('./txt/cm_developer.txt', 'w', encoding='utf-8')
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('dev_href', 'apps_len', 'apps_r_a', 'contact_has', 'category_len', 'privacy_has'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('con_apps_r_a', 'con_apps_r_no_a', 'con_apps_r', 'con_apps_r_no', 'con_apps', 'con_apps_no', 'con_apps_cat_len', 'con_apps_cat_no'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('pri_apps', 'pri_apps_no', 'pri_apps_r', 'pri_apps_r_no', 'pri_apps_r_a', 'pri_apps_r_no_a'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('vid_apps_r', 'vid_apps_r_no', 'vid_apps', 'vid_apps_no', 'vid_apps_r_a', 'vid_apps_r_no_a', 'vid_apps_r_a', 'vid_apps_r_no_a'))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\t'%('web_apps_r', 'web_apps_r_no', 'web_apps', 'web_apps_no', 'web_apps_r_a', 'web_apps_r_no_a'))
    f.write('\n')
    for developer_href in developers:
        apps = developers[developer_href]
        contact_has = 0
        privacy_has = 0
        privacy_apps = 0
        privacy_apps_no = 0
        privacy_apps_rating = 0
        privacy_apps_rating_no = 0
        categories = {}
        contact_apps_category = {}
        contact_apps_category_no = {}
        contact_apps_rating = 0
        contact_apps_rating_no = 0
        contact_apps = 0
        contact_apps_no = 0
        apps_len = len(apps)
        apps_rating = 0
        video_apps_rating = 0
        video_apps_rating_no = 0
        video_apps = 0
        video_apps_no = 0
        website_apps_rating = 0
        website_apps_rating_no = 0
        website_apps = 0
        website_apps_no = 0
        for app_id in apps:
            app = apps[app_id]
            rating_average = check_none(app['rating_average'], 'none')
            if not rating_average == 'none':
                rating_average = float(rating_average)
            else:
                rating_average = 0.0
            apps_rating += rating_average
            category = check_none(app['category'], 'none')
            categories[category] = 1
            developer_privacy = check_none(app['developers']['developer_privacy'], 'none')
            if not developer_privacy == 'none':
                privacy_has = 1
                privacy_apps += 1
                privacy_apps_rating += rating_average
            else:
                privacy_apps_no += 1
                privacy_apps_rating_no += rating_average
            developer_website = check_none(app['developers']['developer_website'], 'none')
            if not developer_website == 'none':
                website_has = 1
                website_apps += 1
                website_apps_rating += rating_average
            else:
                website_apps_no += 1
                website_apps_rating_no += rating_average
            if app.has_key('youtube'):
                youtube = app['youtube']
                video_apps += 1
                video_apps_rating += rating_average
            else:
                video_apps_no += 1
                video_apps_rating_no += rating_average
            if app.has_key('perms') and app['perms'].has_key('contact_perms'):
                contact_perms = app['perms']['contact_perms']
                if 'c' in contact_perms:
                    contact_apps += 1
                    contact_apps_rating += rating_average
                    contact_has = 1
                    contact_apps_category[category] = 1
                else:
                    contact_apps_no += 1
                    contact_apps_rating_no += rating_average
                    contact_apps_category_no[category] = 1
            else:
                contact_apps_no += 1
                contact_apps_rating_no += rating_average
                contact_apps_category_no[category] = 1
        category_len = len(categories)
        apps_rating_average = d_zero(apps_rating, apps_len)
        privacy_apps_rating_average = d_zero(privacy_apps_rating, privacy_apps)
        privacy_apps_rating_no_average = d_zero(privacy_apps_rating_no, privacy_apps_no)
        contact_apps_rating_average = d_zero(contact_apps_rating, contact_apps)
        contact_apps_rating_no_average = d_zero(contact_apps_rating_no, contact_apps_no)
        video_apps_rating_average = d_zero(video_apps_rating, video_apps)
        video_apps_rating_no_average = d_zero(video_apps_rating_no, video_apps_no)
        website_apps_rating_average = d_zero(website_apps_rating, website_apps)
        website_apps_rating_no_average = d_zero(website_apps_rating_no, website_apps_no)
        t = u''
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t'%(t, developer_href, apps_len, apps_rating_average, contact_has, category_len, privacy_has)
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(t, contact_apps_rating_average, contact_apps_rating_no_average, contact_apps_rating, contact_apps_rating_no, contact_apps, contact_apps_no, len(contact_apps_category), len(contact_apps_category_no))
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t'%(t, privacy_apps, privacy_apps_no, privacy_apps_rating, privacy_apps_rating_no, privacy_apps_rating_average, privacy_apps_rating_no_average)
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(t, video_apps_rating, video_apps_rating_no, video_apps, video_apps_no, video_apps_rating_average, video_apps_rating_no_average, video_apps_rating_average, video_apps_rating_no_average)
        t = u'%s%s\t%s\t%s\t%s\t%s\t%s\t'%(t, website_apps_rating, website_apps_rating_no, website_apps, website_apps_no, website_apps_rating_average, website_apps_rating_no_average)
        t = u'%s\n'%(t)
        f.write(t)
    f.close()
    print 'developer_print_apps end'

if __name__ == "__main__":
    #app_contact_init()
    apps = {}
    apps = contact_permission(apps)
    apps = app_permission(apps)
    apps = contact_videos(apps)
    apps = contact_awards(apps)
    apps = contact_share(apps)
    apps = contact_app(apps)
    developers = {}
    developers = developers_apps(apps, developers)
    developers_apps_print(developers)
