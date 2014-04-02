#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import codecs
import sys


def extract(time_difference):
    import os
    import json
    import time
    from datetime import datetime
    from datetime import timedelta as td
    
    import requests

    # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"
    url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson"
    r = requests.get(url)
    data = json.loads(r.text)

    sismos_peru = []
    for i in data['features']:
        obj = {}
        if "Peru" in i['properties']['place'] or "Chile" in i['properties']['place']:
            date = datetime.fromtimestamp(int(i['properties']['time']/1000)).strftime('%H:%M:%S %d %b %Y')
            date_obj = datetime.strptime(date, '%H:%M:%S %d %b %Y') - td(hours=time_difference)
            print date_obj
            sys.exit()
            date += " del " + time.strftime('%d %b', time.localtime(i['properties']['time']/1000))

            if i['properties']['type'] == 'earthquake':
                obj['type'] = "Sismo"
            elif i['properties']['type'] == 'quarry':
                obj['type'] = "Quarry"

            obj['magnitud'] = i['properties']['mag']
            obj['place'] = i['properties']['place']
            obj['date'] = date


        print obj



def main():
    description = u"""Este script extrae sismos para Peru usando datos tomados
    de http://earthquake.usgs.gov/."""

    parser = argparse.ArgumentParser(description=description,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--filename', action='store',
            metavar='file.geojson',
            help=u'''archivo con datos en formato GeoJSON.''',
            required=True, dest='filename')
    parser.add_argument('-s', '--start', action='store',
            metavar='date start',
            help=u'''fecha de inicio YYYY-MM-DD''',
            required=True, dest='date_start')
    parser.add_argument('-e', '--end', action='store',
            metavar='date end',
            help=u'''fecha final YYYY-MM-DD''',
            required=True, dest='date_end')

    args = parser.parse_args()
    filename = args.filename.strip()

    date_start = args.date_start.strip()
    date_end = args.date_end.strip()

    extract(filename, date_start, date_end)



if __name__ == "__main__":
    main()
