RELOAD =

.DEFAULT_GOAL := run


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Commands executed on the host
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

.PHONY: create-network
create-network:
	docker network create verbes

.PHONY: docker-build
docker-build:
	docker build --tag verbes .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -ti \
		--publish 0.0.0.0:5555:5555 \
		--env DATABASE_URL="postgres://postgres@verbes-db:5432/verbs_db" \
		--env DEBUG="y" \
		--env SECRET_KEY='bkw2=gerxsur3h35+p!36pk-vt3$dq=p3cug@a%im)!ys0dcrv' \
		--volume "`pwd`/apps:/app/apps" \
		--volume "`pwd`/verbes:/app/verbes" \
		--user "`id -u`:`id -g`" \
		--net=verbes \
		--name verbes \
		verbes $(CMD)


.PHONY: build-postgres
build-postgres:
	docker run -d \
		--name verbes-db \
		--volume "`pwd`/pg-data":/var/lib/postgresql/data \
		--publish 127.0.0.1:7878:5432 \
		--net=verbes \
		-e POSTGRES_DB=verbs_db \
		postgres:9.4.4

.PHONY: start-postgres
start-postgres:
	docker start verbes-db

.PHONY: stop-postgres
stop-postgres:
	docker stop verbes-db

.PHONY: rm-postgres
rm-postgres:
	docker rm -f verbes-db


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Commands executed in the container
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
