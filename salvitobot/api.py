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

from . import config
from . import _oauth
from . import utils
from .exceptions import NoCountryError


class Bot(object):
    """Main class for Salvitobot.

    This is the only contact point with users.

    """
    def __init__(self):
        self.quake = None
        self.urls = [
            "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson",
            "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
        ]

    def get_quake(self, my_dict=None, country=None):
        """Gets quake info from given dict, or the web.

        Args:
            ``my_dict``: optional, dictionary based on json object from the web
                         service.
            ``country``: required, country to get earthquakes for.

        Raises:
            ``NoCountryError``: if no country is specified for this method.

        """
        if country is None:
            raise NoCountryError('You need to specify one country to get earthquakes for.')

        if my_dict is not None:
            self.quake = utils.parse_quake_data(my_dict, country=country)
        else:
            sismos_peru = []
            for url in self.urls:
                r = requests.get(url)
                data = json.loads(r.text)

                filename = os.path.join(config.base_folder, str(time.time()) + ".json")
                f = codecs.open(filename, "w", "utf-8")
                f.write(json.dumps(data, indent=4))
                f.close()

                parsed_data = utils.parse_quake_data(data, country=country)
                sismos_peru += parsed_data
            self.quake = sismos_peru


def tuit(lista, debug):
    # print lista
    oauth = api.get_oauth()

    users = [
        # 'manubellido',
        # 'aniversarioperu',
        'indeciperu',
        # 'ernestocabralm',
    ]
    for twitter_user in users:
        # send mention
        for obj in lista:
            # status = "@" + twitter_user + " TEST " + message
            # status = message
            status = obj['tuit'] + " cc @" + twitter_user
            # status = message

            # should we tuit this message?
            to_tuit = lib.insert_to_db(status)
            if to_tuit == "do_tuit":

                # print status
                payload = {'status': status}
                url = "https://api.twitter.com/1.1/statuses/update.json"

                try:
                    print("Tweet ", payload)
                    if debug == 0:
                        r = requests.post(url=url, auth=oauth, params=payload)
                        # print json.loads(r.text)['id_str']
                        save_tuit(status)
                except:
                    print("Error")


def create_database():
    filename = os.path.join(config.base_folder, "tuits.db")
    if not os.path.isfile(filename):
        try:
            print("Creating database")
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
            print("DO TUIT: %s" % str(item['tuit']))
            table.insert(item)
            return "do_tuit"
        else:
            print("DONT TUIT: %s" % str(item['tuit']))
            return "dont_tuit"
    else:
        if not table.find_one(url=item['url']):
            print("DO TUIT: %s" % str(item['tuit']))
            table.insert(item)
            return "do_tuit"
        else:
            print("DONT TUIT: %s" % str(item['tuit']))
            return "dont_tuit"
