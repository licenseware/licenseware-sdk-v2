docker_command = COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose-mongo-redis.yml


up:
	$(docker_command) up -d --remove-orphans --force-recreate
down:
	$(docker_command) down


run-prod:	
	uwsgi --http 0.0.0.0:4000 -w main:app --processes 4

run-dev:
	python3 main.py
	
run-mock:
	python3 mock_server.py

run-worker:
	flask worker -p4
	
run-tests:
	rm -rf tests/__pycache__
	python3 -m unittest tests/*
