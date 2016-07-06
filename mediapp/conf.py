# -*- coding: utf-8 -*-

# system
import logging
from logging.handlers import RotatingFileHandler
# pipped
import subliminal
import babelfish
# local
from .settings import LOGFILE, SUBS_LANGUAGES

# logging
def create_logger(logfile=LOGFILE):
    log = logging.getLogger("mediapp")
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.INFO)
    log.addHandler(steam_handler)
    return(log)
LOG = create_logger()


# configure the cache for subliminal
#subliminal.cache_region.configure('dogpile.cache.dbm',
#                                  arguments={'filename': '/tmp/cachefile.dbm'})


# babelfish
BABELFISH_LANG = set()
for lang in SUBS_LANGUAGES:
    BABELFISH_LANG.add(babelfish.Language(lang))


# some helpers
def pluralize(container):
    plural = 's'
    if len(container) == 1:
        plural = ''
    return(plural)

#import ipdb;ipdb.set_trace()
