import os
import re

import dataset
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

        #if not table.find_one(url=item['url'], twitter_user=item['twitter_user']):
        if not table.find_one(url=item['url']):
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
