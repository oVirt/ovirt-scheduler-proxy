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

from API import API
from request_handler import RequestHandler
import SimpleXMLRPCServer
import SocketServer
import os
import logging
from time import strftime


class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn,
                                 SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass


def setup_logging(path):
    logging.basicConfig(level=logging.DEBUG,
                        name="ovirt-scheduler-proxy",
                        format='%(asctime)s %(levelname)-8s [process:%(processName)s,'
                               ' thread:%(threadName)s] %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=path,
                        filemode='w')


class ProxyServer(object):
    def __init__(self):
        self._server = None
        self._handler = None

    def setup(self):
        logging.info("Setting up server")
        self._server = SimpleThreadedXMLRPCServer(("localhost", 18781),
                                                  allow_none=True)

        # TODO make by config
        plugins_path = os.path.join(os.getcwd(), "plugins")
        analyzer_path = os.path.dirname(__file__)

        logging.info("Loading modules from %s" % plugins_path)
        logging.info("Loading analyzer from %s" % analyzer_path)

        self._handler = RequestHandler(
            plugins_path,
            analyzer_path)

    def run(self):
        logging.info("Publishing API")
        self._server.register_introspection_functions()
        self._server.register_instance(API(self._handler))
        self._server.serve_forever()


#for test runs
def main():
    server = ProxyServer()
    server.setup()
    server.run()


if __name__ == "__main__":
    log_filename = '/var/log/ovirt-scheduler-proxy/ovirt-scheduler-proxy.log'
    try:
        setup_logging(log_filename)
    except IOError:
        log_filename = './ovirt-scheduler-proxy.' \
                       + strftime("%Y%m%d_%H%M%S") + '.log'
        setup_logging(log_filename)
    main()
