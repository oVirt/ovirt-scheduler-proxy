#
# Copyright 2013 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

NAME=ovirt-scheduler-proxy
VERSION=0.1
TARBALL=$(NAME)-$(VERSION).tar.gz

tarball:
	tar --xform='s,^,$(NAME)-$(VERSION)/,' -c -z -f $(TARBALL) `git ls-files`

srpm: tarball
	rpmbuild -ts $(TARBALL)

rpm: tarball
	rpmbuild -tb $(TARBALL)

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
	python src/ovirtscheduler/oschedproxyd.py &

stop:
	pkill -f "python src/ovirtscheduler/oschedproxyd.py"

clean:
	find -name "*.pyc" -exec rm {} \;
