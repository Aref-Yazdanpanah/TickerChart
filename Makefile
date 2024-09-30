SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

MAX_LINE_LENGHT := $$(cat "`git rev-parse --show-toplevel`/setup.cfg" | grep "max-line-length" | grep -Eo '[[:digit:]]+' | head -n 1)
LOCAL_DOCKER_COMPOSE = "deployment/local/docker-compose.yml"
PROJECT_NAME = 'TickerChart'

include .env
include .env

lint:
> isort -l $(MAX_LINE_LENGHT) TickerChart
> black -l $(MAX_LINE_LENGHT) .
> flake8 .
.PHONY: lint

local-stack-up:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) up --build
.PHONY: local-stack-up

local-stack-down:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) down
.PHONY: local-stack-down

r:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) restart web
.PHONY: r

python-shell:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) exec web TickerChart/manage.py shell
.PHONY: python-shell

bash:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) exec web bash
.PHONY: bash

psql:
> export `cat .env`
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)
.PHONY: psql

migrate:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) exec web TickerChart/manage.py migrate
.PHONY: migrate

makemigrations:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) exec web TickerChart/manage.py makemigrations
.PHONY: makemigrations

rebuild-web-img:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) build web
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) rm -f web
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) up -d web
.PHONY: rebuild-web-img


show-net-conf:
>	docker-compose -f $(LOCAL_DOCKER_COMPOSE) -p $(PROJECT_NAME) ps  | head -n 2 | tail -n 1 | awk '{printf $$1}' | xargs docker inspect | jq '.[].NetworkSettings.Networks'
.PHONY: show-net-conf
