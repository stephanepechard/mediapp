# -*- coding: utf-8 -*-

# system
import os
import time
# pipped
import psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
# local
from conf import LOG
from settings import MEDIA_DIR, MEDIA_DIR_RECURSIVE
from tasks import fetch_subs


class MediappEventHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        LOG.debug('Filesystem activity detected, triggering task')
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
                self.check_celery()
                time.sleep(10) # arbitrary value, to trigger check_celery() not to often
        except KeyboardInterrupt:
            self.stop()


    def stop(self):
        self.observer.stop()
        self.observer.join() # Wait until the thread terminates.
        LOG.info("Stop watching {}".format(MEDIA_DIR))


    def check_celery(self):
        PROC_NAME = 'celery'
        PROC_ARG = 'mediapp.tasks'

        for proc in psutil.process_iter():
            if proc.name == PROC_NAME and PROC_ARG in proc.cmdline:
                return

        mediapp_proc = psutil.Process(os.getpid())
        celery_path = os.path.join(os.path.dirname(mediapp_proc.exe), PROC_NAME)
        command = '{} -A mediapp.tasks worker'.format(celery_path)
        LOG.warn("Celery does not seem to be running, please start it using:")
        LOG.warn(command)
        LOG.warn("Or using supervisor, see Mediapp's help for instructions.")

