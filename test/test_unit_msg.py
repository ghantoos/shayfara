import unittest
import sys

from shayfara import opts
from shayfara import msg


class TestFunctions(unittest.TestCase):

    def test_msg_01_info(self):
        ''' MSG-01 | info message '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        message = 'test message'
        expected = 'INFO: %s\n' % message
        ret = msg.info(message, args)
        return self.assertEqual(ret, expected)

    def test_msg_02_infov_verbose(self):
        ''' MSG-02 | infov message in verbose mode '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0', '-v']
        args = opts.getopts()
        message = 'test message'
        expected = 'INFO: %s\n' % message
        ret = msg.infov(message, args)
        return self.assertEqual(ret, expected)

    def test_msg_03_infov_no_verbose(self):
        ''' MSG-03 | infov message no verbose (should be silent) '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        message = 'test message'
        expected = ''
        ret = msg.infov(message, args)
        return self.assertEqual(ret, expected)

    def test_msg_04_errx(self):
        ''' MSG-04 | errorx exit message '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        message = 'test message'
        expected = 1
        with self.assertRaises(SystemExit) as cm:
            msg.errx(message, args)
        return self.assertEqual(cm.exception.code, expected)

    def test_msg_05_errn(self):
        ''' MSG-05 | error message '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        message = 'test message'
        expected = 'ERROR: %s\n' % message
        ret = msg.errn(message, args)
        return self.assertEqual(ret, expected)

    def test_msg_06_info(self):
        ''' MSG-06 | warning message '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        message = 'test message'
        expected = 'WARNING: %s\n' % message
        ret = msg.warn(message, args)
        return self.assertEqual(ret, expected)
