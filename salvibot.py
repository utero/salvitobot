#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import config
from datetime import datetime
from datetime import timedelta as td
import re
import sys
#import api

import feedparser
import requests

import extract_quake



def get_tsunami_feed():
    warning = False
    watch = False
    out = False

    url = "http://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml"
    url = r"rss.txt"
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
            print out

def main():
    #time_difference between the server time and Lima
    time_difference = 8
    get_tsunami_feed()
    extract_quake.extract(time_difference)

if __name__ == "__main__":
    main()
