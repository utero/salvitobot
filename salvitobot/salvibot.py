#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta as td
import re
import sys
import json

import feedparser
import requests

import config
import api
from salvitobot.lib import DataExtractor
import lib


def get_tsunami_feed():
    warning = False
    watch = False
    out = False

    tsunamis = []

    url = "http://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml"
    #url = r"rss.txt"
    d = feedparser.parse(url)
    for i in d.entries:
        description = i.description.replace("\n", " ")
        description = re.sub("\s+", " ", description)
        pubdate = datetime.strptime(i.published, '%d %b %Y %H:%M:%S %Z')
        pubdate -= td(hours=5)
        pubdate = pubdate.strftime('%H:%M') + " del " + pubdate.strftime('%d %b')

        pattern = "(A TSUNAMI WARNING IS IN EFFECT FOR(\s+\w+\s*\/*)+)"
        match = re.search(pattern, description, re.M)
        if match:
            if 'PERU' in match.groups()[0]:
                warning = True

        pattern = "(A TSUNAMI WATCH IS IN EFFECT FOR(\s+\w+\s*\/*)+)"
        match = re.search(pattern, description, re.M)
        if match:
            if 'PERU' in match.groups()[0]:
                watch = True

        if warning or watch:
            out = i.category.upper()
            if warning:
                out += ". Alerta de tsunami para PERU "
            if watch:
                out += ". Precaución de tsunami para PERU "
            out += "reportado a las " + str(pubdate) + " "
            out += i.link
            obj['tuit'] = out
            tsunamis.append(obj)
    return tsunamis

def save_tuit(message):
    lib.create_database()
    lib.insert_to_db(message)

def tuit(lista):
    #print lista
    oauth = api.get_oauth()

    users = [
            #'manubellido',
            #'aniversarioperu',
            'indeciperu',
            #'ernestocabralm'
            ]
    for twitter_user in users:
        # send mention
        for obj in lista:
            #status = "@" + twitter_user + " TEST " + message
            #status = message 
            status = obj['tuit'] + " cc @" + twitter_user
            #status = message

            #should we tuit this message?
            to_tuit = lib.insert_to_db(status)
            if to_tuit == "do_tuit":

                #print status
                payload = {
                        'status': status,
                        }
                url = "https://api.twitter.com/1.1/statuses/update.json"

                try:
                    r = requests.post(url=url, auth=oauth, params=payload)
                    #print json.loads(r.text)['id_str']
                    save_tuit(status)
                except:
                    print "Error"

def main():
    #time_difference between the server time and Lima
    time_difference = 1

    print "Buscando tsunamis"
    tsunamis = get_tsunami_feed()
    #print json.dumps(tsunamis, indent=4)

    print "Buscando sismos"
    extractor = DataExtractor()
    sismos = extractor.get_items()
    #print json.dumps(sismos, indent=4)

    if len(sismos) > 0:
        tuit(sismos)
    if len(tsunamis) > 0:
        tuit(tsunamis)

if __name__ == "__main__":
    main()
