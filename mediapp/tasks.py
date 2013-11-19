# -*- coding: utf-8 -*-

# system
import os
import sys
# pipped
from celery import Celery
# libs
import libs.kaa_metadata as kaa_metadata
# local
from settings import MEDIA_DIR, LOG


# celery
#celery = Celery('mediapp.tasks')
#celery.config_from_object('mediapp.celeryconfig')


#@celery.task
def list_media_dir(mediadir, recursive=True):
    media_list = {}
    for mediafile in os.listdir(mediadir):
        mediapath = os.path.join(mediadir, mediafile)
        if os.path.isdir(mediapath):
            if recursive:
                media_list.update(list_media_dir(mediapath))
        else:
            mediadata = kaa_metadata.parse(mediapath)
            if mediadata:
                media_list[mediapath] = mediadata
                LOG.info("File: {}".format(mediapath))
                LOG.info(mediadata)

    return(media_list)


def list_medias(recursive=True):
    LOG.info("Listing medias:")
    media_list = list_media_dir(MEDIA_DIR, recursive)
    LOG.info("Medias found: {}".format(len(media_list)))


list_medias()


#import ipdb;ipdb.set_trace()
