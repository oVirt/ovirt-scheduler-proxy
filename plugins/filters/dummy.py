#!/bin/env python
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

'''
This dummy sample is the most simple filter, it will return all ID's of all the VM's passed over
'''

#do not remove this import, the ovirtsdk is not going to work without it
import ovirtsdk.infrastructure.brokers
from ovirtsdk.xml import params
from sys import stdin

if __name__ == "__main__":
    hosts = params.parseString(stdin.read())

    for host in hosts.host:
        print host.id
