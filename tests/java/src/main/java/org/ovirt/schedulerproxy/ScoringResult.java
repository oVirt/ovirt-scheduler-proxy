package org.ovirt.schedulerproxy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class ScoringResult extends SchedulerResult {
    private HashMap<String, Integer> hostsWithScores = null;

    public void addHost(String host, Integer score) {
        if (hostsWithScores == null) {
            hostsWithScores = new HashMap<String, Integer>();
        }

        hostsWithScores.put(host, score);
    }

    public HashMap<String, Integer> getHosts() {
        return hostsWithScores;
    }
}
