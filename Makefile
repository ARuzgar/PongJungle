all:

git :
	@python3 git.py

build:
	sudo docker compose build

up:
	sudo docker compose up

down:
	sudo docker compose down

logs:
	sudo docker compose logs -f

ps:
	sudo docker compose ps

re:
	make down
	make build
	make up

.PHONY: build up down logs ps git
