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

# do not remove this import, the ovirtsdk is not going to work without it
from ovirtsdk.xml import params
import ovirtsdk.infrastructure.brokers

class SampleFilter():

    def __init__(self):
        pass

    def filter(self, hosts, vm, args):

        my_hosts = params.parseString(hosts)

        acceptedHostsIDs =[]
        for host in my_hosts.host:
            #Do work
            acceptedHostsIDs.append(host.id)

        return acceptedHostsIDs

# Notice: plugin filters are going to run in process that will be created and destroyed
#  per request, you cannot save state in memory
def filterFunction(hosts, vm, args):
    filterClassInstance = SampleFilter()
    #as this will run as a process, communications will be through stdout
    #use log and not print if you want to have debug information
    print filterClassInstance.filter(hosts, vm, args)


#Files can hold all three supported functions (filterFucntion,scoreFunction,balanceFunction)
class SampleScore():
    def __init__(self):
        pass

    def score(self, hosts, vm, args):

        my_hosts = params.parseString(hosts)

        hostScores =[]
        for host in my_hosts.host:
            #Do work
            hostScores.append((host.id,50))

        return hostScores

def scoreFunction(hosts, vm, args):
    scoreClassInstance = SampleScore()
    print scoreClassInstance.score(hosts, vm, args)


def balanceFunction(hosts, args):
    print ['guid']