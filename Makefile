DB_NAME = verbes
DB_CONTAINER_NAME = verbes-db
NETWORK = verbes
RELOAD =


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Commands executed on the host
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

.PHONY: network
network:
	@if ! docker network ls | tail -n +2 | awk '{print $2}' | grep $(NETWORK) > /dev/null; then \
		docker network create $(NETWORK) > /dev/null; \
	fi

.PHONY: build-app
build-app:
	docker build --tag verbes .

.PHONY: run-app
run-app: build-app network
	docker run --rm -ti \
		--publish 0.0.0.0:5555:5555 \
		--env DATABASE_URL="postgres://postgres@$(DB_CONTAINER_NAME):5432/$(DB_NAME)" \
		--env DEBUG="y" \
		--env SECRET_KEY='bkw2=gerxsur3h35+p!36pk-vt3$dq=p3cug@a%im)!ys0dcrv' \
		--volume "`pwd`/apps:/app/apps" \
		--volume "`pwd`/verbes:/app/verbes" \
		--user "`id -u`:`id -g`" \
		--net=$(NETWORK) \
		--name verbes \
		verbes $(CMD)


.PHONY: create-db
create-db: network
	docker create \
		--name $(DB_CONTAINER_NAME) \
		--volume "`pwd`/pg-data":/var/lib/postgresql/data \
		--publish 127.0.0.1:5432:5432 \
		--net=$(NETWORK) \
		-e POSTGRES_DB=$(DB_NAME) \
		postgres:9.5.4

.PHONY: start-db
start-db:
	docker start $(DB_CONTAINER_NAME)

.PHONY: stop-db
stop-db:
	docker stop $(DB_CONTAINER_NAME)

.PHONY: rm-db
rm-db:
	docker rm -f $(DB_CONTAINER_NAME)
