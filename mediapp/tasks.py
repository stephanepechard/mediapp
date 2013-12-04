# -*- coding: utf-8 -*-

# system
import time
# pipped
from celery import Celery
import redis
# local
from celeryconf import REDIS_HOST, REDIS_PORT
from conf import LOG
from fetcher import Fetcher


# celery
celery = Celery('mediapp')
celery.config_from_object('mediapp.celeryconf')
# redis
redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
LOCK_EXPIRE = 60 # Lock expires in 1 minute


@celery.task
def fetch_subs():
    """ This task fetches subtitles for all movies.
        It uses a lock to prevent too many calls at the same time.
        Only one task may be triggered by minute. """

    lock_id = 'mediapp.tasks.fetch_subs'
    if not redis_db.exists(lock_id):
        # set the temporary lock
        redis_db.setex(lock_id, LOCK_EXPIRE, True)

        # fetch subtitles
        new_fetcher = Fetcher()
        new_fetcher.fetch_all_subtitles()
    else:
        LOG.debug('Too many tasks, this one is not triggered!')


@celery.task
def fetch_sub(media_path):
    new_fetcher = Fetcher()
    new_fetcher.fetch_subtitles([media_path])
