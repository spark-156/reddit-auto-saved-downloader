start:
	docker-compose up -d --build

run:
	docker-compose up --build

build:
	docker-compose build

stop:
	docker-compose down

down: stop

