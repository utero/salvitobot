import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRETS_FILE = os.path.join(BASE_DIR, 'config.json')

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        print(error_msg)
        sys.exit()

key = get_secret('key')
secret = get_secret('secret')
token = get_secret('token')
token_secret = get_secret('token_secret')

base_folder = os.path.dirname(__file__)
