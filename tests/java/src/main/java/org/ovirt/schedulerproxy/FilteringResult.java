package org.ovirt.schedulerproxy;

import java.util.LinkedList;
import java.util.List;

public class FilteringResult extends SchedulerResult {
    private List<String> possibleHosts;

    public void addHost(String host) {
        if (possibleHosts == null) {
            possibleHosts = new LinkedList<String>();
        }

        possibleHosts.add(host);
    }

    public List<String> getHosts(){
        return this.possibleHosts;
    }
}
