package org.ovirt.schedulerproxy;

import java.net.MalformedURLException;

import org.apache.xmlrpc.XmlRpcException;
import org.junit.Before;
import org.junit.Test;

public class SchedulerProxyTest {

    SchedulerProxy proxy;

    @Before
    public void setUp() throws MalformedURLException {
        proxy = new SchedulerProxy("http://localhost:18781/");
    }

    @Test
    public void testDiscover() throws XmlRpcException {
        proxy.discover();
    }

    @Test
    public void testFilter() throws XmlRpcException {
        proxy.filter();
    }

    @Test
    public void testScore() throws XmlRpcException {
        proxy.score();
    }

    @Test
    public void testBalance() throws XmlRpcException {
        proxy.balance();
    }
}
