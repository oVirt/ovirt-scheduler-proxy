#
# Copyright 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

NAME=ovirt-scheduler-proxy
VERSION=0.1.3
TARBALL=$(NAME)-$(VERSION).tar.gz

tarball:
	tar --xform='s,^,$(NAME)-$(VERSION)/,' -c -z -f $(TARBALL) `git ls-files`

srpm: tarball
	rpmbuild -ts $(TARBALL)

rpm: tarball
	rpmbuild -tb $(TARBALL)

all: test pep8

test: pythontest javatest

pythontest:
	PYTHONPATH=src:$(PYTHONPATH) nosetests -v

javatest:
	make start;  mvn -f tests/java/pom.xml clean install; make stop

pep8:
	pep8 src

start:
	python src/ovirtscheduler/oschedproxyd.py &

stop:
	pkill -f "python src/ovirtscheduler/oschedproxyd.py"

clean:
	find -name "*.pyc" -exec rm {} \;

restart:
	$(MAKE) stop
	$(MAKE) start
