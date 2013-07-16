package org.ovirt.schedulerproxy;

import java.net.MalformedURLException;
import java.net.URL;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

public class SchedulerProxy {
    final XmlRpcClient client;

    static String HOSTS_EXAMPLE =
            "<hosts><host href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d\" id=\"ce270744-6fb8-4c0c-8e3b-7ded018ee45d\">        <actions>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/deactivate\" rel=\"deactivate\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/approve\" rel=\"approve\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/iscsilogin\" rel=\"iscsilogin\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/iscsidiscover\" rel=\"iscsidiscover\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/commitnetconfig\" rel=\"commitnetconfig\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/fence\" rel=\"fence\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/install\" rel=\"install\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/activate\" rel=\"activate\"/>        </actions>        <name>test</name>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/storage\" rel=\"storage\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/nics\" rel=\"nics\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/tags\" rel=\"tags\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/permissions\" rel=\"permissions\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/statistics\" rel=\"statistics\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/hooks\" rel=\"hooks\"/>        <address>10.35.1.183</address>        <certificate>            <organization>oVirt</organization>            <subject>O=oVirt,CN=10.35.1.183</subject>        </certificate>        <status>            <state>up</state>        </status>        <cluster href=\"/api/clusters/9c3fa7e5-bd04-4aad-9b9e-8ce8a737de1b\" id=\"9c3fa7e5-bd04-4aad-9b9e-8ce8a737de1b\"/>        <port>54321</port>        <type>rhel</type>        <storage_manager priority=\"5\">true</storage_manager>        <version major=\"4\" minor=\"9\" build=\"6\" revision=\"0\" full_version=\"vdsm-4.9.6-44.3.el6_3\"/>        <hardware_information/>        <power_management type=\"alom\">            <enabled>false</enabled>            <options/>        </power_management>        <ksm>            <enabled>true</enabled>        </ksm>        <transparent_hugepages>            <enabled>true</enabled>        </transparent_hugepages>        <iscsi>            <initiator>iqn.1994-05.com.redhat:e03bd23e99a</initiator>        </iscsi>        <cpu>            <topology sockets=\"1\" cores=\"4\"/>            <name>Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz</name>            <speed>1600</speed>        </cpu>        <memory>16601055232</memory>        <max_scheduling_memory>16196304896</max_scheduling_memory>        <summary>            <active>0</active>            <migrating>0</migrating>            <total>0</total>        </summary>        <os type=\"RHEL\">            <version full_version=\"6Server - 6.4.0.4.el6\"/>        </os>        <libvirt_version major=\"0\" minor=\"10\" build=\"2\" revision=\"0\" full_version=\"libvirt-0.10.2-18.el6_4.3\"/>    </host><host href=\"/api/hosts/11111111-6fb8-4c0c-8e3b-7ded018ee45d\" id=\"11111111-6fb8-4c0c-8e3b-7ded018ee45d\">        <actions>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/deactivate\" rel=\"deactivate\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/approve\" rel=\"approve\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/iscsilogin\" rel=\"iscsilogin\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/iscsidiscover\" rel=\"iscsidiscover\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/commitnetconfig\" rel=\"commitnetconfig\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/fence\" rel=\"fence\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/install\" rel=\"install\"/>            <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/activate\" rel=\"activate\"/>        </actions>        <name>test</name>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/storage\" rel=\"storage\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/nics\" rel=\"nics\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/tags\" rel=\"tags\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/permissions\" rel=\"permissions\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/statistics\" rel=\"statistics\"/>        <link href=\"/api/hosts/ce270744-6fb8-4c0c-8e3b-7ded018ee45d/hooks\" rel=\"hooks\"/>        <address>10.35.1.183</address>        <certificate>            <organization>oVirt</organization>            <subject>O=oVirt,CN=10.35.1.183</subject>        </certificate>        <status>            <state>up</state>        </status>        <cluster href=\"/api/clusters/9c3fa7e5-bd04-4aad-9b9e-8ce8a737de1b\" id=\"9c3fa7e5-bd04-4aad-9b9e-8ce8a737de1b\"/>        <port>54321</port>        <type>rhel</type>        <storage_manager priority=\"5\">true</storage_manager>        <version major=\"4\" minor=\"9\" build=\"6\" revision=\"0\" full_version=\"vdsm-4.9.6-44.3.el6_3\"/>        <hardware_information/>        <power_management type=\"alom\">            <enabled>false</enabled>            <options/>        </power_management>        <ksm>            <enabled>true</enabled>        </ksm>        <transparent_hugepages>            <enabled>true</enabled>        </transparent_hugepages>        <iscsi>            <initiator>iqn.1994-05.com.redhat:e03bd23e99a</initiator>        </iscsi>        <cpu>            <topology sockets=\"1\" cores=\"4\"/>            <name>Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz</name>            <speed>1600</speed>        </cpu>        <memory>16601055232</memory>        <max_scheduling_memory>16196304896</max_scheduling_memory>        <summary>            <active>0</active>            <migrating>0</migrating>            <total>0</total>        </summary>        <os type=\"RHEL\">            <version full_version=\"6Server - 6.4.0.4.el6\"/>        </os>        <libvirt_version major=\"0\" minor=\"10\" build=\"2\" revision=\"0\" full_version=\"libvirt-0.10.2-18.el6_4.3\"/>    </host></hosts>";
    static String VM_EXAMPLE = "<vm/>";
    static String FILE_NAME = "dummy";

    public SchedulerProxy(String url) throws MalformedURLException {
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL(url));
        client = new XmlRpcClient();
        client.setConfig(config);
    }

    public void discover() throws XmlRpcException {
        Object execute = client.execute("discover", new Object[] {});
        System.out.println(execute);
    }

    public void filter() throws XmlRpcException {
        Object[] sentObject = new Object[4];
        // filters name
        sentObject[0] = new Object[] { FILE_NAME };
        // hosts xml
        sentObject[1] = HOSTS_EXAMPLE;
        // vm xml
        sentObject[2] = VM_EXAMPLE;
        // additional args
        sentObject[3] = "";

        Object execute = client.execute("runFilters", sentObject);
        System.out.println(parseFilterResult(execute));
    }

    private String parseFilterResult(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("Filter error");
        }
        String retValue = "Got filtered hosts:\n";
        // Its a list of host IDs
        for (Object hostID : (Object[]) result) {
            retValue += hostID.toString() + "\n";
        }
        return retValue;
    }

    public void score() throws XmlRpcException {
        Object[] sentObject = new Object[4];
        // score name + weight pairs
        sentObject[0] = new Object[] { new Object[] { FILE_NAME, 2 } };
        // hosts xml
        sentObject[1] = HOSTS_EXAMPLE;
        // vm xml
        sentObject[2] = VM_EXAMPLE;
        // additional args
        sentObject[3] = "";

        Object execute = client.execute("runCostFunctions", sentObject);
        System.out.println(parseScoreResults(execute));
    }

    private String parseScoreResults(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("Score error");
        }
        String retValue = "Got scored hosts:\n";
        // Its a list of (hostID,score) pairs
        for (Object hostsIDAndScore : (Object[]) result) {
            if (!(hostsIDAndScore instanceof Object[])
                    || ((Object[]) hostsIDAndScore).length != 2) {
                // some kind of error
                System.out.println("Got bad score");
                continue;
            }
            Object[] castedHostsIDAndScore = (Object[]) hostsIDAndScore;
            retValue += castedHostsIDAndScore[0].toString() + " score "
                    + castedHostsIDAndScore[1].toString() + "\n";
        }
        return retValue;
    }

    public void balance() throws XmlRpcException {
        Object[] sentObject = new Object[3];
        // balance name
        sentObject[0] = FILE_NAME;
        // hosts xml
        sentObject[1] = HOSTS_EXAMPLE;
        // additional args
        sentObject[2] = "";

        Object execute = client.execute("runLoadBalancing", sentObject);
        System.out.println(parseBalanceResults(execute));
    }

    private String parseBalanceResults(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("balance error");
        }
        Object[] castedResult = (Object[]) result;
        if (castedResult.length != 1) {
            // is it an error to get more then one vm to balance?
            System.out.println("got more then one vm to balance");
        }
        String retValue = "Got balance vm:\n" + castedResult[0].toString();
        return retValue;
    }
}
