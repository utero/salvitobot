#-*- coding: utf-8 -*-
import codecs
from datetime import datetime
from datetime import timedelta as td
import json
import os
import re
import time

import dataset
import requests
import sqlalchemy

import config


def create_database():
    filename = os.path.join(config.base_folder, "tuits.db")
    if not os.path.isfile(filename):
        try:
            print "Creating database"
            db = dataset.connect('sqlite:///' + filename)
            table = db.create_table("tuits")
            table.create_column('url', sqlalchemy.String)
            table.create_column('tuit', sqlalchemy.String)
            table.create_column('twitter_user', sqlalchemy.String)
        except:
            pass


def insert_to_db(tuit):
    import sys
    import dataset
    filename = os.path.join(config.base_folder, "tuits.db")
    db = dataset.connect("sqlite:///" + filename)
    table = db['tuits']
    
    # line is a line of downloaded data
    match = re.search("(http://.+)", tuit)
    user = re.search("(@\w+)", tuit)

    item = dict()
    item['url'] = match.groups()[0]
    item['tuit'] = tuit
    if user:
        item['twitter_user'] = user.groups()[0]

        if not table.find_one(url=item['url'], twitter_user=item['twitter_user']):
            print "DO TUIT: %s" % str(item['tuit'])
            table.insert(item)
            return "do_tuit"
        else:
            print "DONT TUIT: %s" % str(item['tuit'])
            return "dont_tuit"
    else:
        if not table.find_one(url=item['url']):
            print "DO TUIT: %s" % str(item['tuit'])
            table.insert(item)
            return "do_tuit"
        else:
            print "DONT TUIT: %s" % str(item['tuit'])
            return "dont_tuit"


class DataExtractor(object):

    def __init__(self, url=None):
        if url:
            self.urls = [url]
        else:
            self.urls = [
                "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson",
                "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
            ]

    def get_items(self):
        sismos_peru = []

        for url in self.urls:
            r = requests.get(url)
            data = json.loads(r.text)
    
            filename = os.path.join(config.base_folder, str(time.time()) + ".json")
            f = codecs.open(filename, "w", "utf-8")
            f.write(json.dumps(data, indent=4))
            f.close()
    
            for i in data['features']:
                place = i['properties']['place']
                if "peru" in place.lower() or "chile" in place.lower():
                    obj = {}
                    obj['code'] = i['properties']['code']
                    obj['magnitud'] = i['properties']['mag']
                    obj['magnitud_type'] = i['properties']['magType']

                    # tz: timezone, number of minutes to correct from Epicenter
                    # to UTC
                    obj['tz'] = i['properties']['tz']

                    obj['link'] = i['properties']['url']
                    obj['place'] = i['properties']['place']
                    obj['time'] = i['properties']['time']
                    obj['longitude'] = i['geometry']['coordinates'][0]
                    obj['latitude'] = i['geometry']['coordinates'][1]
                    # depth is in km
                    obj['depth'] = i['geometry']['coordinates'][2]



                    """
                    date = datetime.fromtimestamp(int(i['properties']['time'])/1000).strftime('%H:%M:%S %d %b %Y')
                    date_obj = datetime.strptime(date, '%H:%M:%S %d %b %Y') - td(hours=config.time_difference)
                    date = date_obj.strftime('%H:%M') + " del " + date_obj.strftime('%d %b')
                    obj['date'] = date
                    """
                    sismos_peru.append(obj)
        return sismos_peru
