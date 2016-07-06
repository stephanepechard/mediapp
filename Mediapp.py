#!/usr/bin/env python
# -*- coding: utf-8 -*-

# local
from mediapp.watcher import MediappWatcher


def main():
    watcher = MediappWatcher()
    watcher.start()


if __name__ == '__main__':
    main()
