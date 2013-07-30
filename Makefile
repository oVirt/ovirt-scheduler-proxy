all: test pep8

PYTHONPATH=src

test:
	PYTHONPATH=$(PYTHONPATH) nosetests -v
	make start
	cd tests/java && mvn clean install
	make stop

pep8:
	pep8 src

start:
	python src/oschedproxyd.py &

stop:
	pkill -f "python src/oschedproxyd.py"

clean:
	find -name "*.pyc" -exec rm {} \;
