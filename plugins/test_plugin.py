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


import sys


class test_plugin():
    # Notice: plugin filters are going to run in process that will be created and destroyed
    #  per request, you cannot save state in memory
    def do_filter(self, hosts, vm, args):
        '''This is a simple filter that returns all given host ID'''
        try:
            #use hosts IDs and VM ID to call the Rest API and make a decision

            acceptedHostsIDs = []
            for hostID in hosts:
                #Do work
                acceptedHostsIDs.append(hostID)
            #as this will run as a process, communications will be through stdout
            #use log and not print if you want to have debug information
            print acceptedHostsIDs
        except Exception as ex:
            print >> sys.stderr, ex

    #Files can hold all three supported functions (do_filter, do_score, do_balance)
    def do_score(self, hosts, vm, args):
        '''This is a simple score function that returns all given host ID with score 50'''
        try:
            hostScores = []
            #use hosts IDs and VM ID to call the Rest API and make a decision
            for hostID in hosts:
                #Do work
                hostScores.append((hostID, 50))
            print hostScores
        except Exception as ex:
            print >> sys.stderr, ex

    def do_balance(self, hosts, args):
        '''This is a fake balance function that always return the guid 33333333-3333-3333-3333-333333333333'''
        try:
            #use hosts IDs to call the Rest API and make a decision
            #return the wanted vm and a list of underutilised hosts
            print ('33333333-3333-3333-3333-333333333333', ['11111111-1111-1111-1111-111111111111'])
        except Exception as ex:
            print >> sys.stderr, ex
