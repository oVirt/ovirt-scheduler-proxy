package org.ovirt.schedulerproxy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class SchedulerResult {
    private Map<String, List<String>> pluginErrors = null;
    private int resultCode = 0;
    private LinkedList<String> errorMessages = null;

    public Map<String, List<String>> getPluginErrors() {
        return this.pluginErrors;
    }

    public void addPluginErrors(String pluginName, String errorMessage) {
        if (pluginErrors == null) {
            pluginErrors = new HashMap<String, List<String>>();
        }

        if (pluginErrors.get(pluginName) == null) {
            pluginErrors.put(pluginName, new LinkedList<String>());
        }

        pluginErrors.get(pluginName).add(errorMessage);
    }

    public void addError(String errorMessage) {
        if (errorMessages == null) {
            errorMessages = new LinkedList<String>();
        }
    }

    public List<String> getErrors() {
        return this.errorMessages;
    }

    public void setResultCode(int statusCode) {
        this.resultCode = statusCode;
    }

    public int getResultCode() {
        return this.resultCode;
    }

}
