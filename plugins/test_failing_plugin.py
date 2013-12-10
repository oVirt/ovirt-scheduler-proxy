class test_failing_plugin(object):
    def do_filter(self, hosts, vm, args):
        """This filter is expected to fail and should be used only in tests."""
        raise Exception("Expected fail")

    def do_score(self, hosts, vm, args):
        """This function is expected to fail and should be used only in tests."""

        raise Exception("Expected fail")
