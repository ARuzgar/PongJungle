all: clean re

clean:
	clear

git:
	@python3 git.py

build:
	sudo docker compose build

up:
	sudo docker compose up

down:
	sudo docker compose down

ps:
	sudo docker compose ps

re: down build up

logs:
	sudo docker compose logs -f

logs-backend:
	sudo docker logs --tail 100 -f backend

logs-api42:
	sudo docker logs --tail 100 -f api42

logs-game:
	sudo docker logs --tail 100 -f game

logs-frontend:
	sudo docker logs --tail 100 -f frontend

logs-chat:
	sudo docker logs --tail 100 -f chat

.PHONY: all clean git build up down logs ps logs-backend logs-api42 logs-game logs-frontend logs-chat