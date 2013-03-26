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
db_review = sqlite3.connect('db_app_review.db')

#######################################
sql_review_simple = '''
SELECT review_id, app_id, reviewer, date, device, version, review_star
FROM review
'''
def user_review_score(apps):
    print 'user_review_score start'
    c = db_review.cursor()
    c.execute(sql_review_simple, ())
    r = c.fetchone()
    while r != None:
        review_id = r[0].strip().lower()
        app_id = r[1].lower().strip()
        reviewer = r[2].lower().strip()
        date = r[3].lower().strip()
        device = r[4].lower().strip()
        app_version = r[5].lower().strip()
        review_score = r[6].lower().strip()
        if app_version == '' or review_score == '':
            r = c.fetchone()
            continue
        if not apps.has_key(app_id):
            apps[app_id] = {}
        if not apps[app_id].has_key('user_reviews'):
            apps[app_id]['user_reviews'] = {}
        if not apps[app_id]['user_reviews'].has_key(app_version):
            apps[app_id]['user_reviews'][app_version] = {}
        if not apps[app_id]['user_reviews'][app_version].has_key(review_id):
            apps[app_id]['user_reviews'][app_version][review_id] = {}
        apps[app_id]['user_reviews'][app_version][review_id]['reviewer'] = reviewer
        apps[app_id]['user_reviews'][app_version][review_id]['date'] = date
        apps[app_id]['user_reviews'][app_version][review_id]['device'] = device
        apps[app_id]['user_reviews'][app_version][review_id]['review_score'] = review_score
        r = c.fetchone()
    c.close()
    print len(apps)
    print 'user_review_score end'
    return apps

def apps_detail_get(apps):
    print 'app_details_get start'
    sql = 'SELECT app_id, category, price, rating_average, installs FROM app WHERE developer_href IS NOT NULL'
    c = db.cursor()
    c.execute(sql, ())
    r = c.fetchone()
    i = 0
    while r != None:
        i = i + 1
        app_id = r[0].lower().strip()
        category = r[1].lower().strip()
        price = r[2].lower().strip()
        rating_average = r[3].lower().strip()
        installs = r[4].lower().strip()
        if not apps.has_key(app_id):
            r = c.fetchone()
            continue
        print app_id, i
        if category == 'arcade & action':
            category = 'arcade and action'
        if category == 'cards & casino':
            category = 'cards and casino'
        price = price_c(price)
        apps[app_id]['category'] = category
        apps[app_id]['price'] = price
        apps[app_id]['rating_average'] = rating_average
        apps[app_id]['installs'] = installs
        r = c.fetchone()
    print 'app_details_get end'
    return apps

def review_app_category_print(apps):
    print 'review_app_category_print start'
    f = codecs.open('./txt_user_review/review_app_category.txt', 'w', encoding='utf-8')
    t = u'app_id\tcategory\tprice\trating_average\tinstalls\tversions\t\n'
    f.write(t)
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 10)
        app = apps[app_id]
        if not app.has_key('category'):
            category = 'none'
        else:
            category = app['category']
        if not app.has_key('price'):
            price = 'none'
        else:
            price = app['price']
        if not app.has_key('rating_average'):
            rating_average = 'none'
        else:
            rating_average = app['rating_average']
        if not app.has_key('installs'):
            installs = 'none'
        else:
            installs = app['installs']
        if not app.has_key('user_reviews'):
            versions = 0
        else:
            versions = len(app['user_reviews'])
        t = u'%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, category, price, rating_average, installs, versions)
        f.write(t)
    f.close()
    print 'review_app_category_print end'



def user_review_score_aggregate_print(apps):
    print 'review_app_category_print start'
    f = codecs.open('./txt_user_review/user_review_score_aggregate.txt', 'w', encoding='utf-8')
    t = u'app_id\tcategory\tprice\trating_average\tinstalls\tversions\tapp_version\treviews_count\taverage_review_score\n'
    f.write(t)
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 10)
        app = apps[app_id]
        if not app.has_key('category'):
            category = 'none'
        else:
            category = app['category']
        if not app.has_key('price'):
            price = 'none'
        else:
            price = app['price']
        if not app.has_key('rating_average'):
            rating_average = 'none'
        else:
            rating_average = app['rating_average']
        if not app.has_key('installs'):
            installs = 'none'
        else:
            installs = app['installs']
        if not app.has_key('user_reviews'):
            versions = 0
        else:
            versions = len(app['user_reviews'])
        reviews = app['user_reviews']
        for app_version in reviews:
            review_count = len(reviews[app_version])
            if review_count == 0:
                continue
            review_score_total = 0.0
            reviews_version = reviews[app_version]
            for review_id in reviews_version:
                review = reviews_version[review_id]
                reviewer = review['reviewer']
                date = review['date']
                device = review['device']
                review_score = review['review_score']
                review_score_total = float(review_score)
            review_score_average = review_score_total/review_count
            t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, category, price, rating_average, installs, versions, app_version, review_count, review_score_average)
            f.write(t)
    f.close()
    print 'user_review_score_aggreagte_print end'

################################################



def user_review_score_each_print(apps):
    print 'user_review_score_each_print start'
    f = codecs.open('./txt_user_review/user_review_score.txt', 'w', encoding='utf-8')
    t = u'app_id\tcategory\tprice\trating_average\tinstalls\tversions\tapp_version\treview_id\treviewer\tdate\tdevice\treview_score\n'
    f.write(t)
    i_t = len(apps)
    i_i = 0
    p = 0
    for app_id in apps:
        p, i_i = p_percent(p, i_i, i_t, 10)
        app = apps[app_id]
        if not app.has_key('category'):
            category = 'none'
        else:
            category = app['category']
        if not app.has_key('price'):
            price = 'none'
        else:
            price = app['price']
        if not app.has_key('rating_average'):
            rating_average = 'none'
        else:
            rating_average = app['rating_average']
        if not app.has_key('installs'):
            installs = 'none'
        else:
            installs = app['installs']
        if not app.has_key('user_reviews'):
            versions = 0
        else:
            versions = len(app['user_reviews'])
        reviews = app['user_reviews']
        for app_version in reviews:
            reviews_version = reviews[app_version]
            for review_id in reviews_version:
                review = reviews_version[review_id]
                reviewer = review['reviewer']
                date = review['date']
                device = review['device']
                review_score = review['review_score']
                t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, category, price, rating_average, installs, versions, app_version, review_id, reviewer, date, device, review_score)
                f.write(t)
    f.close()
    print 'user_review_score_each_print end'



#com.catstudio.sogmw
sql_review_full = '''
SELECT review_id, app_id, reviewer, date, device, version, review_star, title, comment 
FROM review WHERE app_id = '%s'
'''
def user_review_full():
    print 'user_review_full start'
    f = codecs.open('./txt_user_review/user_review_full.txt', 'w', encoding='utf-8')
    t = u'app_id\tapp_version\treview_id\treviewer\tdate\tdevice\treview_score\ttitle\tcomment\n'
    f.write(t)
    c = db_review.cursor()
    c.execute(sql_review_full%('com.catstudio.sogmw'),( ))
    r = c.fetchone()
    while r != None:
        review_id = r[0].strip().lower()
        app_id = r[1].lower().strip()
        reviewer = r[2].lower().strip()
        date = r[3].lower().strip()
        device = r[4].lower().strip()
        app_version = r[5].lower().strip()
        review_score = r[6].lower().strip()
        title = r[7].lower().strip()
        comment = r[8].lower().strip()
        print app_version, review_score
        if app_version == '' or review_score == '':
            r = c.fetchone()
            continue
        t = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(app_id, app_version, review_id, reviewer, date, device, review_score, title, comment)
        f.write(t)
        r = c.fetchone()
    c.close()
    print 'user_review_full end'
                
#######################################
if __name__ == '__main__':
    #### user review category file
    #apps = {}
    #apps = user_review_score(apps)
    #apps = apps_detail_get(apps)
    #review_app_category_print(apps)
    #### user review score aggregate
    #apps = {}
    #apps = user_review_score(apps)
    #apps = apps_detail_get(apps)
    #user_review_score_aggregate_print(apps)
    #### user review score each
    #apps = {}
    #apps = user_review_score(apps)
    #apps = apps_detail_get(apps)
    #user_review_score_each_print(apps)
    #### user review full out by name
    user_review_full()
