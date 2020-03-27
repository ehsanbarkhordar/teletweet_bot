import configparser
import os

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './config.ini')
config.read(filename)
