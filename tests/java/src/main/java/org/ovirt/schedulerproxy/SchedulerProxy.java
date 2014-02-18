package org.ovirt.schedulerproxy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Map;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

public class SchedulerProxy {
    final XmlRpcClient client;
    private final int RESULT_OK = 0;

    public SchedulerProxy(String url) throws MalformedURLException {
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL(url));
        client = new XmlRpcClient();
        client.setConfig(config);
    }

    public HashMap<String, HashMap<String, String[]>> discover() throws XmlRpcException {
        Object execute = client.execute("discover", new Object[]{});
        return parseDiscover(execute);
    }

    private Object parseRawResult(Object xmlRpcStruct, SchedulerResult result) {
        /* new response format
        {
          "result_code": int,
          "result": [list of UUIDS],
          "plugin_errors": { "plugin_name": ["errormsgs"] },
          "errors": ["errormsgs"]
        }
        */

        if (!(xmlRpcStruct instanceof HashMap)) {
            return null;
        }

        @SuppressWarnings("unchecked")
        Map<String, Object> castedResult = (HashMap<String, Object>) xmlRpcStruct;

        // keys will be status_code, plugin_errors, errors and result
        result.setResultCode((Integer) castedResult.get("result_code"));
        Map<String, Object[]> plugin_errors = null;
        Object[] errors = null;

        if (result.getResultCode() != RESULT_OK) {
            plugin_errors = (HashMap<String, Object[]>)castedResult.get("plugin_errors");
            errors = (Object[])castedResult.get("errors");

            if (plugin_errors != null) {
                for (Map.Entry<String, Object[]> entry: plugin_errors.entrySet()) {
                    for (Object errorMsg: entry.getValue()) {
                        result.addPluginErrors(entry.getKey(), errorMsg.toString());
                    }
                }
            }

            if (errors != null) {
                for (Object msg: errors) {
                    result.addError((String)msg);
                }
            }
        }

        /* returns just result without any headers
           so it can be passed to the old parsers
         */
        return castedResult.get("result");
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

    public FilteringResult filter(String[] filterNames, String[] HostID, String vmID, String args) throws XmlRpcException {
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

    private FilteringResult parseFilterResult(Object xmlRpcStruct) {
        FilteringResult retValue = new FilteringResult();
        Object rawResult = parseRawResult(xmlRpcStruct, retValue);
        if (rawResult == null) {
            System.out.println("filter error");
            return null;
        }

        // Its a list of host IDs
        for (Object hostID : (Object[]) rawResult) {
            retValue.addHost(hostID.toString());
        }
        return retValue;
    }

    public ScoringResult score(String[] scoreNames,
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

    private ScoringResult parseScoreResults(Object xmlRpcStruct) {
        ScoringResult result = new ScoringResult();
        Object rawResults = parseRawResult(xmlRpcStruct, result);
        if (rawResults == null) {
            System.out.println("Score error");
            return null;
        }

        HashMap<String, Integer> retValue = new HashMap<String, Integer>();
        // Its a list of (hostID,score) pairs
        for (Object hostsIDAndScore : (Object[]) rawResults) {
            if (!(hostsIDAndScore instanceof Object[]) || ((Object[]) hostsIDAndScore).length != 2) {
                // some kind of error
                System.out.println("Got bad score");
                return null;
            }
            Object[] castedHostsIDAndScore = (Object[]) hostsIDAndScore;
            result.addHost(castedHostsIDAndScore[0].toString(), (Integer) castedHostsIDAndScore[1]);
        }
        return result;
    }

    public BalanceResult balance(String balanceName, String[] HostID, String args)
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

    private BalanceResult parseBalanceResults(Object xmlRpcStruct) {
        BalanceResult result = new BalanceResult();
        Object rawResults = parseRawResult(xmlRpcStruct, result);
        if (xmlRpcStruct == null) {
            System.out.println("balance error");
            return null;
        }
        Object[] castedResult = (Object[]) rawResults;
        HashMap<String, List<String>> retValue = new HashMap<String, List<String>>();
        for (Object hostID : (Object[]) castedResult[1]) {
            result.addHost(hostID.toString());
        }
        result.setVmToMigrate(castedResult[0].toString());
        return result;
    }
}
