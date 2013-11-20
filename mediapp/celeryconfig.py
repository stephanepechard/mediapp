# -*- coding: utf-8 -*-

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/0'
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_IMPORTS = ('mediapp.tasks')
CELERYD_CONCURRENCY = 1
