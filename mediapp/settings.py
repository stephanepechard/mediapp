# -*- coding: utf-8 -*-

# directory where media are located
MEDIA_DIR = '/home/stephane/mov'

# should we look recursively?
MEDIA_DIR_RECURSIVE = False

# language representation from 3-letter code (ISO-639-3)
SUBS_LANGUAGES = ['eng', 'fra']

# default logfile name and location
import os
LOGFILE = os.path.join(os.getcwd(), 'log_mediapp.log')
