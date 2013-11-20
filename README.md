Mediapp
=======
`Mediapp` automatically finds subtitles for your videos.
Downloads are triggered by file system activity, so each time you
add, rename or remove a file in your specified media directory,
`Mediapp` will try to find new subtitles, in the languages you want.


Installation
------------
Clone this repo:

    git clone https://github.com/stephanepechard/mediapp.git

and install dependencies through `virtualenv`:

    make


Configuration
-------------
Before launching it, you can configure `Mediapp` with the dedicated file
`settings.py`. In it, you'll find:

- `MEDIA_DIR`: the directory your videos are in ;
- `MEDIA_DIR_RECURSIVE`: to indicate if the subtitles fetching should be
recursive or not ;
- `SUBS_LANGUAGES`: the list of language representation
(3-letter code, ISO-639-3) for the subtitles ;
- `LOGFILE`: the logfile of `Mediapp`.


Automatic launch through `supervisor`
-------------------------------------
A `supervisor` script is provided to do everything automatically for you.
Just edit the `command`, `directory` and `user` lines (once for `mediapp_py`,
once for `mediapp_celery`) to match your installation paths.
Then link the file to `supervisor` configuration. On Debian, just type:

    sudo ln -s /etc/supervisor/conf.d/mediapp.conf supervisord.conf

and you're good to go after a small `supervisor` reload.


Manual launch through your fingers
----------------------------------
You need to launch two things: `Mediapp` itself and `celery`,
both into the `virtualenv` you created during installation.
To launch `Mediapp`, just type:

    (venv) user@localhost $ ./venv/bin/python Mediapp.py

To launch `celery`, just type:

    (venv) user@localhost $ ./venv/bin/celery -A mediapp.tasks worker


How it works
------------
`Mediapp` makes use of several libraries:

- [subliminal](http://subliminal.readthedocs.org/) to determine and download
the right subtitles ;
- [celery](http://www.celeryproject.org/) to do it asynchronously ;
- [watchdog](http://pythonhosted.org/watchdog/) to monitor file system events.


Future works
------------
A static report on what movies the directory contains is on its way.

License
-------
GPL v3
