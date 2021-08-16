# This file is used for testing pieces of code 

from iqoptionapi.stable_api import IQ_Option
from configparser import ConfigParser
import time

config = ConfigParser()
config.read('config.ini')

print(config['account']['email'], config['account']['password'])