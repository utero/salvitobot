import datetime

import pytz


def parse_quake_data(data, country):
    """Extract info about earthquake.

    Args:
        ``data``: dict object as downloaded from web service.
        ``country``: string, country to look for earthquake for

    Returns:
        list of earthquakes.

    """
    quakes = []
    country = country.lower()
    for i in data['features']:
        place = i['properties']['place']
        if country in place.lower():
            obj = dict()
            obj['code'] = i['properties']['code']
            obj['magnitude'] = i['properties']['mag']
            obj['magnitude_type'] = i['properties']['magType']

            # tz: timezone, Timezone offset from UTC in minutes
            obj['tz'] = i['properties']['tz']
            obj['type'] = i['properties']['type']

            obj['link'] = i['properties']['url']
            obj['place'] = i['properties']['place']
            obj['time'] = i['properties']['time']
            obj['longitude'] = i['geometry']['coordinates'][0]
            obj['latitude'] = i['geometry']['coordinates'][1]
            # depth is in km
            obj['depth'] = i['geometry']['coordinates'][2]

            obj['datetime_utc'] = datetime.datetime.fromtimestamp(obj['time'] / 1000, pytz.utc)

            out = "SISMO"
            out += ". " + str(obj['magnitude']) + " grados " + obj['magnitude_type']
            out += " en " + obj['place']
            out += ". A horas "
            out += " " + obj['link']

            obj['tuit'] = out
            quakes.append(obj)
    return quakes
