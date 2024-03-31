lint:
	pylint *.py

test:
	pytest *.py

build:
	python3 generate.py
