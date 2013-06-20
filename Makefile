all: test pep8

PYTHONPATH=src

test:
	PYTHONPATH=$(PYTHONPATH) nosetests -v

pep8:
	pep8 src
