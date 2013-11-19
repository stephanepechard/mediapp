# -*- coding: utf-8 -*-

MEDIA_DIR = '/home/stephane/mov'

# you can comment (or delete) the next line if it is the same as MEDIA_DIR
DL_DIR = '/media/data/bt/done'



# default log file
import os
LOGFILE = os.path.join(os.getcwd(), 'mediapp.log')

# logging setup
import logging
from logging.handlers import RotatingFileHandler
LOG = logging.getLogger("mediapp")
LOG.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler(LOGFILE, 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
LOG.addHandler(steam_handler)
