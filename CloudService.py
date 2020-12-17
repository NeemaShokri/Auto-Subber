import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

api_key = config['account']['api_key']
print(api_key)