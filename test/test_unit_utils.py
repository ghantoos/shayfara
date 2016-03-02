import unittest
import sys
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


from shayfara import opts
from shayfara import utils


def return_input(string):
    """ generate a random string """
    return string


class TestFunctions(unittest.TestCase):

    def test_utils_01_load_files_skip_dir(self):
        ''' UTL-01 | load_files: skip directory if -r not specified '''
        sys.argv = ['shayfara', '-e', '--no-recursive', 'test/dirtest']
        args = opts.getopts()
        expected = []
        ret = utils.load_files(args)
        return self.assertEqual(ret, expected)

    def test_utils_02_load_files_skip_dir(self):
        ''' UTL-02 | load_files: skip directory if not exists '''
        sys.argv = ['shayfara', '-e', 'foo/']
        args = opts.getopts()
        expected = []
        ret = utils.load_files(args)
        return self.assertEqual(ret, expected)

    def test_utils_03_load_files_access_read_error(self):
        ''' UTL-03 | load_files: exit if access error '''
        sys.argv = ['shayfara', '-e', '/etc/shadow']
        args = opts.getopts()
        expected = 1
        with self.assertRaises(SystemExit) as cm:
            utils.load_files(args)
        return self.assertEqual(cm.exception.code, expected)

    def test_utils_04_load_files_access_write_error(self):
        ''' UTL-04 | load_files: exit if access error '''
        sys.argv = ['shayfara', '-e', '/etc/motd']
        args = opts.getopts()
        expected = 1
        with self.assertRaises(SystemExit) as cm:
            utils.load_files(args)
        return self.assertEqual(cm.exception.code, expected)

    def test_utils_05_check_file_access_no_access(self):
        ''' UTL-05 | check_file_access: file with no access, return 1 '''
        sys.argv = ['shayfara', '-e', '/etc/motd']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = 1
        ret = utils.check_file_access(ifile)
        return self.assertEqual(ret, expected)

    def test_utils_06_check_file_access_access(self):
        ''' UTL-06 | check_file_access: file access ok, return 0 '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = 0
        ret = utils.check_file_access(ifile)
        return self.assertEqual(ret, expected)

    def test_utils_07_get_output_file_enc(self):
        ''' UTL-07 | get_output_file: default encrypt extension: .enc '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = '%s.enc' % ifile
        ret = utils.get_output_file(ifile, args)
        return self.assertEqual(ret, expected)

    def test_utils_08_get_output_file_dec(self):
        ''' UTL-08 | get_output_file: default decrypt extension: .dec '''
        sys.argv = ['shayfara', '-d', 'test/dirtest/file0']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = '%s.dec' % ifile
        ret = utils.get_output_file(ifile, args)
        return self.assertEqual(ret, expected)

    def test_utils_09_get_output_file(self):
        ''' UTL-09 | get_output_file: user defined extension: .foo '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0', '-E', 'foo']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = '%s.foo' % ifile
        ret = utils.get_output_file(ifile, args)
        return self.assertEqual(ret, expected)

    def test_utils_10_get_password_command_line(self):
        ''' UTL-10 | get_password: from command line '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0', '-P', 'mypassword']
        args = opts.getopts()
        expected = 'mypassword'
        ret = utils.get_password(args)
        return self.assertEqual(ret, expected)

    def test_utils_11_get_password_file_not_exists(self):
        ''' UTL-11 | get_password: from password file, not exists, exit '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0',
                    '-p', 'tests/passwordfoo']
        args = opts.getopts()
        expected = 1
        with self.assertRaises(SystemExit) as cm:
            utils.get_password(args)
        return self.assertEqual(cm.exception.code, expected)

    def test_utils_12_get_password_command_line(self):
        ''' UTL-12 | get_password: from password file '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0',
                    '-p', 'test/passwordfile']
        args = opts.getopts()
        expected = 'mypassword'
        ret = utils.get_password(args)
        return self.assertEqual(ret, expected)

    @patch('getpass.getpass', return_value='mypassword')
    def test_utils_13_get_password_user_prompt(self, input):
        ''' UTL-13 | get_password: from user prompt '''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        expected = 'mypassword'
        ret = utils.get_password(args)
        return self.assertEqual(ret, expected)

    # mocking getpass function to return its input, i.e:
    # 'Password: ' then 'Re-enter password: ', to simulate
    # a user entering two different passwords
    @patch('getpass.getpass', side_effect=return_input)
    def test_utils_14_get_password_user_prompt(self, input):
        ''' UTL-14 | get_password: from user prompt, not matching'''
        sys.argv = ['shayfara', '-e', 'test/dirtest/file0']
        args = opts.getopts()
        expected = 1
        with self.assertRaises(SystemExit) as cm:
            utils.get_password(args)
        return self.assertEqual(cm.exception.code, expected)

    def test_utils_15_get_output_file_dec(self):
        ''' UTL-15 | get_output_file: directory and in-place
            should have no extension
        '''
        sys.argv = ['shayfara', '-d', 'test/dirtest/file0',
                    '-D', '/tmp/foo/', '--in-place']
        args = opts.getopts()
        ifile = args.FILES[0]
        expected = ifile
        ret = utils.get_output_file(ifile, args)
        return self.assertEqual(ret, expected)
