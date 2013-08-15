package org.ovirt.schedulerproxy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.net.MalformedURLException;
import java.net.URL;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

public class SchedulerProxy {
    final XmlRpcClient client;

    public SchedulerProxy(String url) throws MalformedURLException {
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL(url));
        client = new XmlRpcClient();
        client.setConfig(config);
    }

    public HashMap<String, HashMap<String, String[]>> discover() throws XmlRpcException {
        Object execute = client.execute("discover", new Object[] {});
        return parseDiscover(execute);
    }

    private HashMap<String, HashMap<String, String[]>> parseDiscover(Object result) {
        if (result == null || !(result instanceof HashMap)) {
            System.out.println("discover error");
            return null;
        }
        HashMap<String, HashMap<String, Object[]>> castedResult = (HashMap<String, HashMap<String, Object[]>>) result;
        // Its a list of host IDs
        HashMap<String, HashMap<String, String[]>> retValue = new HashMap<String, HashMap<String, String[]>>();
        for (String keyType : castedResult.keySet()) {
            HashMap<String, Object[]> typeMap = castedResult.get(keyType);
            HashMap<String, String[]> newTypeMap = new HashMap<String, String[]>();
            for (String keyModuleName : typeMap.keySet()) {
                String[] keys = new String[2];
                for (int i = 0; i < 2; i++) {
                    keys[i] = (String) typeMap.get(keyModuleName)[i];
                }
                newTypeMap.put(keyModuleName, keys);
            }
            retValue.put(keyType, newTypeMap);
        }
        return retValue;
    }

    public List<String> filter(String[] filterNames, String[] HostID, String vmID, String args) throws XmlRpcException {
        Object[] sentObject = new Object[4];
        // filters name
        sentObject[0] = filterNames;
        // hosts xml
        sentObject[1] = HostID;
        // vm xml
        sentObject[2] = vmID;
        // additional args
        sentObject[3] = args;

        Object execute = client.execute("runFilters", sentObject);
        return parseFilterResult(execute);
    }

    private List<String> parseFilterResult(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("Filter error");
            return null;
        }
        // Its a list of host IDs
        List<String> retValue = new LinkedList<String>();
        for (Object hostID : (Object[]) result) {
            retValue.add(hostID.toString());
        }
        return retValue;
    }

    public HashMap<String, Integer> score(String[] scoreNames,
            Integer[] weights,
            String[] HostID,
            String vmID,
            String args) throws XmlRpcException {
        Object[] sentObject = new Object[4];

        if (scoreNames == null || weights == null || scoreNames.length != weights.length) {
            return null;
        }

        Object[] pairs = new Object[scoreNames.length];

        for (int i = 0; i < pairs.length; i++) {
            pairs[i] = new Object[] { scoreNames[i], weights[i] };
        }
        // score name + weight pairs
        sentObject[0] = pairs;
        // hosts xml
        sentObject[1] = HostID;
        // vm xml
        sentObject[2] = vmID;
        // additional args
        sentObject[3] = args;

        Object execute = client.execute("runCostFunctions", sentObject);
        return parseScoreResults(execute);
    }

    private HashMap<String, Integer> parseScoreResults(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("Score error");
        }
        HashMap<String, Integer> retValue = new HashMap<String, Integer>();
        // Its a list of (hostID,score) pairs
        for (Object hostsIDAndScore : (Object[]) result) {
            if (!(hostsIDAndScore instanceof Object[]) || ((Object[]) hostsIDAndScore).length != 2) {
                // some kind of error
                System.out.println("Got bad score");
                return null;
            }
            Object[] castedHostsIDAndScore = (Object[]) hostsIDAndScore;
            retValue.put(castedHostsIDAndScore[0].toString(), (Integer) castedHostsIDAndScore[1]);
        }
        return retValue;
    }

    public HashMap<String, List<String>> balance(String balanceName, String[] HostID, String args)
            throws XmlRpcException {
        Object[] sentObject = new Object[3];
        // balance name
        sentObject[0] = balanceName;
        // hosts xml
        sentObject[1] = HostID;
        // additional args
        sentObject[2] = args;

        Object execute = client.execute("runLoadBalancing", sentObject);
        return parseBalanceResults(execute);
    }

    private HashMap<String, List<String>> parseBalanceResults(Object result) {
        if (result == null || !(result instanceof Object[])) {
            System.out.println("balance error");
        }
        Object[] castedResult = (Object[]) result;
        HashMap<String, List<String>> retValue = new HashMap<String, List<String>>();
        List<String> hostIDs = new LinkedList<String>();
        for (Object hostID : (Object[]) castedResult[1]) {
            hostIDs.add(hostID.toString());
        }
        retValue.put(castedResult[0].toString(), hostIDs);
        return retValue;
    }
}