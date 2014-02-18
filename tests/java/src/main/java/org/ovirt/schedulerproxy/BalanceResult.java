package org.ovirt.schedulerproxy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class BalanceResult extends SchedulerResult {
    private Map<String, List<String>> balancingData= null;
    private List<String> underUtilizedHosts = null;
    private String vmToMigrate = null;

    public void addHost(String host) {
        if (underUtilizedHosts == null) {
            underUtilizedHosts = new LinkedList<String>();
        }

        underUtilizedHosts.add(host);
    }

    public void setVmToMigrate(String vm) {
        this.vmToMigrate = vm;
    }


    public Map<String, List<String>> getResult() {
        if (balancingData == null) {
            balancingData = new HashMap<String, List<String>>();
        }

        balancingData.put(this.vmToMigrate, underUtilizedHosts);
        return balancingData;
    }
}
