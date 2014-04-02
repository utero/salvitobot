#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import config
import re
import sys
#import api

import feedparser
import requests



def get_tsunami_feed():
    warning = False
    watch = False
    out = False

    url = "http://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml"
    #url = r"rss.txt"
    d = feedparser.parse(url)
    for i in d.entries:
        description = i.description.replace("\n", " ")
        description = re.sub("\s+", " ", description)

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
            out = i.category
            if warning:
                out += ". Alerta de tsunami para PERU "
            if watch:
                out += ". Precaución de tsunami para PERU "
            out += i.link
            print out

def main():
    get_tsunami_feed()

if __name__ == "__main__":
    main()
