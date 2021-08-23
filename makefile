docker_command = COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose-mongo-redis.yml


up:
	$(docker_command) up -d --remove-orphans --force-recreate
down:
	$(docker_command) down


prod:	
	uwsgi --http 0.0.0.0:4000 -w main:app --processes 4

dev:
	python3 main.py
	
mock:
	python3 mock_server.py

worker:
	flask worker -p4
	
test:
	rm -rf tests/__pycache__
	python3 -m unittest tests/*
