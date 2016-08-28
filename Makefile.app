.DEFAULT_GOAL := run

.PHONY: collectstatic
collectstatic:
	python manage.py collectstatic --clear --no-input

.PHONY: createsuperuser
createsuperuser:
	python manage.py createsuperuser

.PHONY: load-most-frequent-verbs
load-most-frequent-verbs:
	python manage.py loaddata most_frequent_verbs.json

.PHONY: load-tenses
load-tenses:
	python manage.py loaddata mood_tense_person.json

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations verbes

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: run
run: collectstatic migrate
	gunicorn --bind 0.0.0.0:5555 --workers 3 $(RELOAD) verbes.wsgi
