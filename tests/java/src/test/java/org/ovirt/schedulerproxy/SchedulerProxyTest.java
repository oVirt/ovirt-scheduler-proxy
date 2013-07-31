package org.ovirt.schedulerproxy;


import static org.junit.Assert.assertTrue;
import java.net.MalformedURLException;
import java.util.HashMap;
import java.util.List;

import org.apache.xmlrpc.XmlRpcException;
import org.junit.Before;
import org.junit.Test;

public class SchedulerProxyTest {
	
	static String FILE_NAME = "dummy";
	static String HOST_ID1 = "11111111-1111-1111-1111-111111111111";
	static String HOST_ID2 = "22222222-2222-2222-2222-222222222222";
	static String[] HOST_ARRAY = new String[] { HOST_ID1, HOST_ID2 };
	static String VM_ID  = "33333333-3333-3333-3333-333333333333";
	static String BALANCE_RESULT = "33333333-3333-3333-3333-333333333333";

	SchedulerProxy proxy;

	@Before
	public void setUp() throws MalformedURLException {
		proxy = new SchedulerProxy("http://localhost:18781/");
	}

	@Test
	public void testDiscover() throws XmlRpcException {
		HashMap<String, List<String>> result = proxy.discover();
		assertTrue(result.containsKey("filters"));
		assertTrue(result.get("filters").contains(FILE_NAME));
		assertTrue(result.containsKey("scores"));
		assertTrue(result.get("scores").contains(FILE_NAME));
		assertTrue(result.containsKey("filters"));
		assertTrue(result.get("balance").contains(FILE_NAME));
		
	}
	
	@Test
	public void testFilter() throws XmlRpcException {
		List<String> result = proxy.filter(new String[] { FILE_NAME }, HOST_ARRAY, VM_ID, "");
		assertTrue(result.size() == 2);
		assertTrue(result.contains(HOST_ID1));
		assertTrue(result.contains(HOST_ID2));
	}
	
	@Test
	public void testScore() throws XmlRpcException {
		HashMap<String,Integer> result = proxy.score(new String[] { FILE_NAME }, new Integer[] { 2 }, HOST_ARRAY, VM_ID, "");
		assertTrue(result.size() == 2);
		assertTrue(result.get(HOST_ID1) == 100);
		assertTrue(result.get(HOST_ID2) == 100);
	}
	
	@Test
	public void testBalance() throws XmlRpcException {
		String result = proxy.balance(FILE_NAME, HOST_ARRAY, "");
		assertTrue(result.equals(BALANCE_RESULT));
	}
}