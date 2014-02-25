from ovirtsdk.xml import params
from ovirtsdk.api import API
import sys


class even_vm_distribution():
    '''rank hosts by the number of running vms on them, with the least first'''

    properties_validation = ''

    def _get_connection(self):
        #open a connection to the rest api
        connection = None
        try:
            connection = API(url='http://host:port',
                             username='user@domain', password='')
        except BaseException as ex:
            #letting the external proxy know there was an error
            print >> sys.stderr, ex
            return None

        return connection

    def _get_hosts(self, host_ids, connection):
        #get all the hosts with the given ids
        engine_hosts = connection.hosts.list(
            query=" or ".join(["id=%s" % u for u in host_ids]))

        return engine_hosts

    def do_score(self, hosts_ids, vm_id, args_map):
        conn = self._get_connection()
        if conn is None:
            return

        engine_hosts = self._get_hosts(hosts_ids, conn)

        #iterate over them and score them based on the number of vms running
        host_scores = []
        for engine_host in engine_hosts:
            if(engine_host and
                    engine_host.summary):
                host_scores.append((engine_host.id,
                                    engine_host.summary.active))
        print host_scores
