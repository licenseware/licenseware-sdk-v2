run-main:	
	python3 main.py
	
run-mock:
	python3 mock_server.py
	
run-tests:
	rm -rf tests/__pycache__
	python3 -m unittest tests/*