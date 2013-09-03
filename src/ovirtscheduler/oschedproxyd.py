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

from API import API
from request_handler import RequestHandler
import SimpleXMLRPCServer
import SocketServer
import os
import logging
from logging.handlers import RotatingFileHandler
from time import strftime


class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn,
                                 SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass


def setup_logging(path):
    file_handler = RotatingFileHandler(path,
                                       maxBytes=50*1024,
                                       backupCount=6)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s'
                                      ' [process:%(processName)s,'
                                      ' thread:%(threadName)s] '
                                      '%(message)s',
                                      '%a, %d %b %Y %H:%M:%S')
    file_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)


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
