Mediapp
=======
Mediapp automatically finds subtitles for your videos. It uses 


Installation
------------
Clone this repo:

    git clone https://github.com/stephanepechard/mediapp.git

and install dependencies through `virtualenv`:

    make


Automatic launch through `supervisor`
-------------------------------------
A `supervisor` script is provided to do everything automatically for you. Just edit the `command`, `directory` and `user` lines (once for `mediapp_py`, once for `mediapp_celery`) to match your installation paths. Then link the file to `supervisor` configuration. On Debian, just type:

    sudo ln -s /etc/supervisor/conf.d/mediapp.conf supervisord.conf

and you're good to go after a small `supervisor` reload.


Manual launch through your fingers
----------------------------------
You need to launch two things: `Mediapp` itself and `celery`, both into the `virtualenv` you created during installation. To launch `Mediapp`, just type:

    (venv) user@localhost $ ./venv/bin/python Mediapp.py

To launch `celery`, just type:

    (venv) user@localhost $ ./venv/bin/celery -A mediapp.tasks worker
