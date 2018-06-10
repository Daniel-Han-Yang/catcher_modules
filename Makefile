make:
	python setup.py bdist_wheel

install: make
	sudo pip install dist/catcher_modules-*

tests:
	python -m pytest --capture=sys --ignore=postgres-data

deploy: make
	twine upload dist/*

.PHONY: install
