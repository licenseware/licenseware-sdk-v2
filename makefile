docker_command = COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose-mongo-redis.yml


up:
	$(docker_command) up -d --remove-orphans --force-recreate
down:
	$(docker_command) down


run-main:	
	python3 main.py
	
run-mock:
	python3 mock_server.py
	
run-tests:
	rm -rf tests/__pycache__
	python3 -m unittest tests/*
