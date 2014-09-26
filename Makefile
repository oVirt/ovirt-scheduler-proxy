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
VERSION=$(shell cat VERSION | tr -d '\n')
LASTVERSION=$(shell git describe --match='[[:digit:]].[[:digit:]].[[:digit:]]*' --abbrev=0 --tags | tr -d '\n' | sed 's/-/.0./' | tr - .)
GITVER=$(shell git describe  --match='[[:digit:]].[[:digit:]].[[:digit:]]*' --tags | sed 's/-/.0./' | tr - .)
TARBALL=$(NAME)-$(VERSION).tar.gz

AUTHOR=$(shell git config user.name)
EMAIL=$(shell git config user.email)

all: test pep8

version:
	if [ "x$(GITVER)" != "x" ]; then echo -ne "$(GITVER)" > VERSION; fi

$(NAME).spec: VERSION $(NAME).spec.in
	sed -e 's/{VERSION}/$(VERSION)/g' $(NAME).spec.in >$@

dist: tarball

tarball: version $(TARBALL)

$(TARBALL): VERSION $(NAME).spec
	tar --xform='s,^,$(NAME)-$(VERSION)/,' -c -z -f $(TARBALL) `git ls-files` $(NAME).spec

bumpver:
	@build-aux/bumpver.sh "$(LASTVERSION)" >VERSION
	@echo "Version bumped from $(LASTVERSION) to $(VERSION)"

tag:
	git tag $(VERSION)

changelog:
	@if grep '$(VERSION)-1' $(NAME).spec.in; then true; else \
	echo "Create a changelog entry first:" && \
	echo "* $(shell LANG=C date +"%a %b %d %Y") $(AUTHOR) <$(EMAIL)> $(VERSION)-1" && \
	false; fi

release: checkclean bumpver all changelog commit tag $(TARBALL)
	@echo "Release $(VERSION) created successfully."
	@echo "Push using git push origin HEAD:refs/for/master"
	@echo "Once reviewed push tags using git push $(VERSION)"

checkclean:
	@echo "Checking if there are no uncommited changes..."
	@if git status --porcelain | egrep -v "^( M VERSION| M $(NAME).spec.in)" | egrep -v "^\\?\\?"; then false; else true; fi

commit:
	git commit -a -m "Release of version $(VERSION)"

srpm: version tarball
	rpmbuild -ts $(TARBALL)

rpm: version tarball
	rpmbuild -tb $(TARBALL)

test: pythontest javatest

pythontest:
	OSCHEDPROXY_PLUGINS=$(PWD)/tests/plugins PYTHONPATH=src:$(PYTHONPATH) nosetests -v

javatest:
	OSCHEDPROXY_PLUGINS=$(PWD)/tests/plugins make start;  mvn -f tests/java/pom.xml clean install; make stop

pep8:
	pep8 src

start:
	OSCHEDPROXY_PLUGINS=$(PWD)/tests/plugins python src/ovirtscheduler/oschedproxyd.py &

stop:
	pkill -f "python src/ovirtscheduler/oschedproxyd.py"

clean:
	find -name '*.pyc' -exec rm {} \;

restart:
	$(MAKE) stop
	$(MAKE) start

.PHONY: checkclean commit version bumpver release all test pythontest javatest start stop pep8 clean restart rpm srpm tag tarball
