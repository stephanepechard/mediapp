# -*- coding: utf-8 -*-

# system
import os
# pipped
import subliminal
from subliminal.video import scan_videos
# libs
import libs.kaa_metadata as kaa_metadata
# local
from conf import LOG, BABELFISH_LANG, pluralize
from settings import MEDIA_DIR, MEDIA_DIR_RECURSIVE


class Fetcher(object):

    media_list = {}

    def list_media_dir(self, media_dir, recursive=True):
        for media_file in sorted(os.listdir(media_dir), key=str.lower):
            media_path = os.path.join(media_dir, media_file)
            if os.path.isdir(media_path):
                if recursive:
                    self.media_list.update(list_media_dir(media_path))
            else:
                media_data = kaa_metadata.parse(media_path)
                if media_data:
                    self.media_list[media_path] = media_data
                    LOG.info("File: {}".format(media_path))


    def list_medias(self, recursive=True):
        LOG.info("Listing medias:")
        self.list_media_dir(MEDIA_DIR, recursive)
        LOG.info("{} video{} files found".format(len(self.media_list),
                                                 pluralize(self.media_list)))


    def find_sub_file(self, media_path):
        found = False
        media_dir = os.path.dirname(media_path)
        media_name, media_ext = os.path.splitext(os.path.basename(media_path))
        for sub in sorted(os.listdir(media_dir), key=str.lower):
            sub_path = os.path.join(media_dir, sub)
            if sub_path != media_path and os.path.isfile(sub_path):
                sub_name, sub_ext = os.path.splitext(sub)
                if sub_name.startswith(media_name) and \
                    sub_ext in subliminal.video.SUBTITLE_EXTENSIONS:
                        found = True

        return(found)


    def find_movies_without_subtitles(self):
        no_subs = {}
        for media in self.media_list:
            if self.media_list[media]['subtitles']:
                LOG.debug("Found subs embedded into " + media)
            elif self.find_sub_file(media):
                LOG.debug("Found subs file for " + media)
            else:
                no_subs.update({media: self.media_list[media]})
        return(no_subs)


    def fetch_subtitles(self, media_dict):
        vids = media_dict.keys() if isinstance(media_dict, dict) else media_dict
        subs = scan_videos(vids, subtitles=True, embedded_subtitles=False)
        single = True if len(BABELFISH_LANG) == 1 else False
        subliminal.download_best_subtitles(subs, BABELFISH_LANG, single=single)


    def fetch_all_subtitles(self):
        self.list_medias(MEDIA_DIR_RECURSIVE)
        no_subs = self.find_movies_without_subtitles()
        if no_subs:
            self.fetch_subtitles(no_subs)
            subs = self.find_movies_without_subtitles()
            new_subs = [sub for sub in no_subs.keys() if sub not in subs.keys()]
            if new_subs:
                for sub in new_subs:
                    LOG.info("Found new subs for " + sub)
                LOG.info("{} new subtitles found".format(len(new_subs)))
