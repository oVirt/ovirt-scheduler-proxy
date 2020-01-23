#!/usr/bin/python3
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

# USAGE:
#
#   To create an external scheduler plugin your file must have at least one of
#   the following functions: filterFunction, scoreFunction, balanceFunction.
#   If you wish to supply a description and parameters regex you can also
#   create a description function: describeScore/describeScore/describeBalance.
#
#   Remember that communication to the external scheduler will occur through
#   stdout/stderr because the plugin will run as a separate process.
#   So use print instead of return, and print(msg, file=sys.stderr) instead of
#   throwing an exception

from __future__ import print_function
import sys


class test_plugin():
    # Notice: plugin filters are going to run in process that will be created
    # and destroyed per request, you cannot save state in memory
    def do_filter(self, hosts, vm, args):
        """This is a simple filter that returns all given host ID"""
        try:
            # use hosts IDs and VM ID to call the Rest API and make a decision

            acceptedHostsIDs = []
            for hostID in hosts:
                # Do work
                acceptedHostsIDs.append(hostID)
            # as this will run as a process, communications will be through
            # stdout use log and not print if you want to have
            # debug information
            print(acceptedHostsIDs)
        except Exception as ex:
            print(ex, file=sys.stderr)

    # Files can hold all three supported functions (do_filter,
    # do_score, do_balance)
    def do_score(self, hosts, vm, args):
        """This is a simple score function that returns all given host ID with score 50"""
        try:
            hostScores = []
            # use hosts IDs and VM ID to call the Rest API and make a decision
            for hostID in hosts:
                # Do work
                hostScores.append((hostID, 50))
            print(hostScores)
        except Exception as ex:
            print(ex, file=sys.stderr)

    def do_balance(self, hosts, args):
        """This is a fake balance function that always return the guid 33333333-3333-3333-3333-333333333333"""
        try:
            # use hosts IDs to call the Rest API and make a decision
            # return the wanted vm and a list of underutilised hosts
            print(('33333333-3333-3333-3333-333333333333', ['11111111-1111-1111-1111-111111111111']))
        except Exception as ex:
            print(ex, file=sys.stderr)
