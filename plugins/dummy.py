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

# USAGE:
#
#   To create an external scheduler plugin your file must have at least one of the
#   following functions: filterFunction, scoreFunction, balanceFunction.
#   If you wish to supply a description and parameters regex you can also
#   create a description function: describeScore/describeScore/describeBalance.
#
#   Remember that communication to the external scheduler will occur through
#   stdout/stderr because the plugin will run as a separate process.
#   So use print instead of return, and print >> sys.stderr instead of
#   throwing an exception


# do not remove this import, the ovirtsdk is not going to work without it
from ovirtsdk.xml import params
from ovirtsdk import api
import ovirtsdk.infrastructure.brokers
import sys


class SampleFilter():

    def __init__(self):
        pass

    def filter(self, hosts, vm, args):

        #use hosts IDs and VM ID to call the Rest API and make a decision

        acceptedHostsIDs = []
        for hostID in hosts:
            #Do work
            acceptedHostsIDs.append(hostID)

        return acceptedHostsIDs


# Notice: plugin filters are going to run in process that will be created and destroyed
#  per request, you cannot save state in memory
def filterFunction(hosts, vm, args):
    '''This is a simple filter that returns all given host ID'''
    try:
        filterClassInstance = SampleFilter()
        #as this will run as a process, communications will be through stdout
        #use log and not print if you want to have debug information
        print filterClassInstance.filter(hosts, vm, args)
    except Exception as ex:
        print >> sys.stderr, ex

regex_filter = ""


#Files can hold all three supported functions (filterFucntion,scoreFunction,balanceFunction)
class SampleScore():
    def __init__(self):
        pass

    def score(self, hosts, vm, args):

        hostScores = []
        #use hosts IDs and VM ID to call the Rest API and make a decision
        '''
            Sample code:
            #take from configuration
            api = API(url='http://host:port', username='user@domain', password='password')
            for id in hosts:
                hostObject = api.hosts.get(query='id=' + id)

            ... etc
        '''
        for hostID in hosts:
            #Do work
            hostScores.append((hostID, 50))

        return hostScores


def scoreFunction(hosts, vm, args):
    '''This is a simple score function that returns all given host ID with score 50'''
    try:
        scoreClassInstance = SampleScore()
        print scoreClassInstance.score(hosts, vm, args)
    except Exception as ex:
        print >> sys.stderr, ex

regex_score = ""


class SampleBalance():
    def __init__(self):
        pass

    def balance(self, hosts, args):
        #use hosts IDs to call the Rest API and make a decision
        #return the wanted vm and a list of underutilised hosts
        return '33333333-3333-3333-3333-333333333333', ['11111111-1111-1111-1111-111111111111']


def balanceFunction(hosts, args):
    '''This is a fake balance function that always return the guid 33333333-3333-3333-3333-333333333333'''
    try:
        balanceInstance = SampleBalance()
        print balanceInstance.balance(hosts, args)
    except Exception as ex:
        print >> sys.stderr, ex

regex_balance = ""