all: down build-processor up setup-db

build-processor:
	docker-compose build processor

run-simulator:
	docker-compose build simulator
	docker-compose up simulator

up:
	docker-compose up -d mysql grafana processor

down:
	docker-compose down

setup-db:
	docker-compose up -d mysql
	docker-compose run processor python3 setup.py
