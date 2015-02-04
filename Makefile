help:
	@echo "test - run all tests"

test:
	coverage run --source salvitobot setup.py test
