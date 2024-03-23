all: clean cloudfree down build up

prune:
	sudo docker system prune -a -f

cloudfree:
	sh cloudflare_cache_clear.sh

login_api42:
	sudo docker exec -it api42 bash

login_dbapi42:
	sudo docker exec -it dbapi42 bash -c "psql -h dbapi42 -U api -d apiusers"

login_dbbackend:
	sudo docker exec -it dbbackend bash -c "psql -h dbbackend -U user1 -d backend"

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

.PHONY: all clean git build up down logs ps login_api42 login_dbapi42 login_backend logs-backend logs-api42 logs-game logs-frontend logs-chat cloudfree