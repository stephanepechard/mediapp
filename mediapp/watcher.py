# -*- coding: utf-8 -*-

# system
import time
# pipped
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
# local
from conf import LOG
from settings import MEDIA_DIR, MEDIA_DIR_RECURSIVE
from tasks import fetch_subs


class MediappEventHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        LOG.debug('Trigger task')
        fetch_subs.delay()


class MediappWatcher(object):

    observer = Observer()

    def start(self):
        event_handler = MediappEventHandler()
        self.observer.schedule(event_handler, path=MEDIA_DIR, recursive=MEDIA_DIR_RECURSIVE)

        LOG.info("Start watching {}".format(MEDIA_DIR))
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


    def stop(self):
        self.observer.stop()
        self.observer.join() # Wait until the thread terminates.
        LOG.info("Stop watching {}".format(MEDIA_DIR))
