import fileinput
import api
import requests


for line in fileinput.input():
    oauth = api.get_oauth()

    line = line.strip()

    url = "https://api.twitter.com/1.1/statuses/destroy/"
    url += line + ".json"

    r = requests.post(url, auth=oauth)
