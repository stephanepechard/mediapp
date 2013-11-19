# -*- coding: utf-8 -*-

# system
import time
# pipped
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
# local
from .settings import MEDIA_DIR


def launch_watcher(recursive=False):
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MEDIA_DIR, recursive)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
