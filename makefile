docker_command = COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose-mongo-redis.yml


up:
	$(docker_command) up -d --remove-orphans --force-recreate
down:
	$(docker_command) down


prod:	
	uwsgi --http 0.0.0.0:4000 -w main:app --processes 4

dev:
	rm -rf tests/__pycache__
	python3 -m unittest tests/test_sdk_cli.py
	python3 main.py
	
mock:
	uwsgi --http 0.0.0.0:5000 -w mock_server:app --processes 4

worker:
	flask worker -p4
	
test:
	rm -rf tests/__pycache__
	python3 -m unittest tests/test_sdk_cli.py
	rm -rf tests/__pycache__
	python3 -m unittest tests/*
	rm -rf app

dev-docs:
	pdoc --http : app

docs:
	pdoc --html --output-dir app-docs app


dev-sdk-docs:
	pdoc --http : licenseware

sdk-docs:
	pdoc --html --output-dir docs licenseware
	