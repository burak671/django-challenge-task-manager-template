PYTHON ?= python

.PHONY: install migrate run test

install:
	$(PYTHON) -m pip install -r requirements.txt

migrate:
	$(PYTHON) manage.py migrate

run:
	$(PYTHON) manage.py runserver

test:
	$(PYTHON) manage.py test
