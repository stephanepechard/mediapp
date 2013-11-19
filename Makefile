all: dev

venv:
	[ -e venv/bin/pip ] || virtualenv venv

dev: venv
	./venv/bin/pip install -r requirements.txt
