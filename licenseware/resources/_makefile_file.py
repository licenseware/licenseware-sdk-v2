docker_command = COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose-mongo-redis.yml


up:
	$(docker_command) up -d --remove-orphans --force-recreate
down:
	$(docker_command) down


prod:	
	uwsgi --http 0.0.0.0:5000 -w main:app --processes 4

mock:
	uwsgi --http 0.0.0.0:4000 -w mock_server:app --processes 4

dev:
	python3 main.py

worker:
	dramatiq main:App.broker -p4 --watch ./
	
test:
	echo create some tests

dev-docs:
	pdoc --http : app

docs:
	pdoc --html --output-dir docs app



# SDK

sdk-dev:
	rm -rf tests/__pycache__
	python3 -m unittest tests/test_sdk_cli.py
	python3 main.py
	
sdk-test:
	echo "Make sure to start mock_server first and you have test_files folder available"
	rm -rf tests/__pycache__
	python3 -m unittest tests/test_sdk_cli.py
	rm -rf tests/__pycache__
	python3 -m unittest tests/*
	rm -rf docker-compose-mongo-redis.yml
	rm -rf main_example.py
	rm -rf main.py
	rm -rf app.log
	rm -rf app
	

sdk-dev-docs:
	pdoc --http : licenseware

sdk-docs:
	pdoc --html --output-dir sdk-docs licenseware
	

install-sdk:
	pip3 uninstall -y licenseware
	python3 setup.py bdist_wheel sdist
	pip3 install ./dist/licenseware-2.0.0-py3-none-any.whl
	rm -rf build
	rm -rf licenseware.egg-info
	rm -rf wheel_sdk
	mv dist wheel_sdk 


build-wheel:
	python3 setup.py bdist_wheel sdist
	rm -rf build
	rm -rf licenseware.egg-info 
	mv dist wheel_sdk 
