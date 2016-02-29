import unittest
import sys

from shayfara import opts


class TestFunctions(unittest.TestCase):

    def test_opts_01_default_cipher(self):
        ''' OPT-01 | default cipher is simplecrypt '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0', '-v']
        ret = vars(opts.getopts())['cipher']
        return self.assertIn('simplecrypt', ret)

    def test_opts_02_default_output_plugin(self):
        ''' OPT-02 | default output plug-in is local '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0', '-v']
        ret = vars(opts.getopts())['plugin']
        return self.assertIn('local', ret)
