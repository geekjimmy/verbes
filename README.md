# Verbes

Verbes is a French verb conjugation trainer.

![](img/preparions.png)

![](img/preparions-feedback.png)

![](img/results.png)


# Development Environment

## Quick Start

### Create the database image

```
$ make create-db
```

### Start the database

```
$ make start-db
```

### Create initial data

```
$ make run-app CMD=bash
# The following commands must be run in the app container
$ make migrate
$ make createsuperuser
$ make load-tenses load-most-frequent-verbs
$ exit
```

### Run the app

```
$ make run-app
```

#### Reload on change

Restart gunicorn workers when code changes.

```
$ make run-app CMD=bash
$ make run OPTIONS=--reload  # In the container
```

# Deployment

On the Dokku host:

```
$ dokku apps:create verbes.mathieularose.com
$ dokku config:set verbes.mathieularose.com SECRET_KEY=<secret key>
$ dokku postgres:create verbes
$ sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
$ dokku postgres:link verbes verbes.mathieularose.com
$ dokku proxy:ports-add verbes.mathieularose.com http:80:5555
```

## HTTPS

```
$ dokku config:set --no-restart verbes.mathieularose.com DOKKU_LETSENCRYPT_EMAIL=<e-mail>
$ sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
$ dokku letsencrypt verbes.mathieularose.com
$ dokku letsencrypt:cron-job --add
```


# Author

Mathieu Larose <mathieu@mathieularose.com>
