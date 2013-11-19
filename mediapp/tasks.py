# -*- coding: utf-8 -*-

# system
from datetime import timedelta
import os
import sys
# pipped
from babelfish import Language
from celery import Celery
import subliminal
# libs
import libs.kaa_metadata as kaa_metadata
# local
from conf import LOG, BABELFISH_LANGUAGES
from settings import MEDIA_DIR, MEDIA_DIR_RECURSIVE



# celery
#celery = Celery('mediapp.tasks')
#celery.config_from_object('mediapp.celeryconfig')


def list_media_dir(mediadir, recursive=True):
    media_list = {}
    for mediafile in sorted(os.listdir(mediadir), key=str.lower):
        mediapath = os.path.join(mediadir, mediafile)
        if os.path.isdir(mediapath):
            if recursive:
                media_list.update(list_media_dir(mediapath))
        else:
            mediadata = kaa_metadata.parse(mediapath)
            if mediadata:
                media_list[mediapath] = mediadata
                LOG.info("File: {}".format(mediapath))
                #LOG.debug(mediadata)

    return(media_list)


#@celery.task
def list_medias(recursive=True):
    LOG.info("Listing medias:")
    media_list = list_media_dir(MEDIA_DIR, recursive)
    LOG.info("{} movies found".format(len(media_list)))
    return(media_list)


def find_sub_file(media_path):
    found = False
    media_dir = os.path.dirname(media_path)
    media_name, media_ext = os.path.splitext(os.path.basename(media_path))
    for sub in sorted(os.listdir(media_dir), key=str.lower):
        sub_path = os.path.join(media_dir, sub)
        if sub_path != media_path and os.path.isfile(sub_path):
            sub_name, sub_ext = os.path.splitext(sub)
            if sub_name == media_name and sub_ext in subliminal.video.SUBTITLE_EXTENSIONS:
                found = True

    return(found)


def find_subtitles(media_list):
    no_subs = {}
    for media in media_list:
        if media_list[media]['subtitles']:
            LOG.debug("Found subs embedded into " + media)
        elif find_sub_file(media):
            LOG.debug("Found subs file for " + media)
        else:
            no_subs.update({media: media_list[media]})
    return(no_subs)


def fetch_subtitle(no_subs):
    videos = subliminal.video.scan_videos(no_subs.keys(),
                                          subtitles=True,
                                          embedded_subtitles=False)
    subliminal.download_best_subtitles(videos, BABELFISH_LANGUAGES, single=True)

    still_no_subs = find_subtitles(no_subs)
    new_subs = [sub for sub in no_subs.keys() if sub not in still_no_subs.keys()]
    for subs in new_subs:
        LOG.info("Found subs for " + subs)
    if new_subs:
        LOG.info("{} subtitles found".format(len(new_subs)))


media_list = list_medias(MEDIA_DIR_RECURSIVE)
no_subs = find_subtitles(media_list)
if no_subs:
    fetch_subtitle(no_subs)

#import ipdb;ipdb.set_trace()

