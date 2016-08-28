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


# Author

Mathieu Larose <mathieu@mathieularose.com>
