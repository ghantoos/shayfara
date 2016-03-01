import unittest
import os
import sys
import shutil
import tempfile

from shayfara import opts
from shayfara import utils
from shayfara.plugins import local


class TestFunctions(unittest.TestCase):

    ''' initialize the local plugin '''
    plugin = local.ShayfaraPlugin()

    def test_plugins_local_01_write(self):
        ''' LOC-01 | local: write file - success '''
        data = b'Some data'
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        # write data in file
        ret = self.plugin.write(filename, data)
        # delete file
        os.remove(filename)
        return self.assertEqual(ret, filename)

    def test_plugins_local_02_write_fail(self):
        ''' LOC-02 | local: write file - failure '''
        data = 'Some data'
        filename = '/etc/motd'
        # write data in file
        ret = self.plugin.write(filename, data)
        return self.assertEqual(ret, None)

    def test_plugins_local_03_delete(self):
        ''' LOC-03 | local: delete file - success '''
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        # delete file
        ret = self.plugin.remove(filename)
        return self.assertEqual(ret, filename)

    def test_plugins_local_04_delete_fail(self):
        ''' LOC-04 | local: delete file - failure '''
        # DON'T RUN THIS AS ROOT!!
        filename = '/etc/motd'
        # delete file
        ret = self.plugin.remove(filename)
        return self.assertEqual(ret, None)

    def test_plugins_local_05_rename(self):
        ''' LOC-05 | local: rename file - success '''
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        # rename file
        newname = filename + 'foo'
        ret = self.plugin.rename(filename, newname)
        # delete file
        os.remove(newname)
        return self.assertEqual(ret, newname)

    def test_plugins_local_06_rename_fail(self):
        ''' LOC-06 | local: rename file - failure '''
        # DON'T RUN THIS AS ROOT!!
        filename = '/etc/motd'
        # rename file
        newname = filename + 'foo'
        ret = self.plugin.rename(filename, newname)
        return self.assertEqual(ret, None)

    def test_plugins_local_07_updatedir(self):
        ''' LOC-07 | local: updatedir - success '''
        try:
            with tempfile.TemporaryDirectory(delete=False) as d:
                directory = d.name
        except:
            directory = tempfile.mkdtemp()

        sys.argv = ['shayfara', '-e', '-D', directory, 'test/dirtest/']
        args = opts.getopts()
        # get directory file list
        files = utils.load_files(args)
        files.sort()
        expected = '%s/dir1/file1' % directory
        # update directory
        ret = self.plugin.updatedir(files[0], args.dest_dir, args.FILES[0])
        # cleanup
        shutil.rmtree(directory)
        return self.assertEqual(ret, expected)

    def test_plugins_local_08_updatedir_failure_permission(self):
        ''' LOC-08 | local: updatedir - failure permission '''
        directory = '/var/log/'
        sys.argv = ['shayfara', '-e', '-D', directory, 'test/dirtest/']
        args = opts.getopts()
        # get directory file list
        files = utils.load_files(args)
        expected = 1
        # update directory
        with self.assertRaises(SystemExit) as cm:
            self.plugin.updatedir(files[1], args.dest_dir, args.FILES[0])
        return self.assertEqual(cm.exception.code, expected)

    def test_plugins_local_09_updatedir_failure_no_dir(self):
        ''' LOC-09 | local: updatedir - failure no such directory '''
        directory = '/foo'
        sys.argv = ['shayfara', '-e', '-D', directory, 'test/dirtest/']
        args = opts.getopts()
        # get directory file list
        files = utils.load_files(args)
        expected = 1
        # update directory
        with self.assertRaises(SystemExit) as cm:
            self.plugin.updatedir(files[1], args.dest_dir, args.FILES[0])
        return self.assertEqual(cm.exception.code, expected)

    def test_plugins_local_13_updatedir(self):
        ''' LOC-13 | local: updatedir - force directory '''
        try:
            with tempfile.TemporaryDirectory(delete=True) as d:
                directory = d.name
        except:
            directory = tempfile.mkdtemp()
        shutil.rmtree(directory)

        sys.argv = ['shayfara', '-e', '-D', directory,
                    'test/dirtest/', '-f']
        args = opts.getopts()
        # get directory file list
        files = utils.load_files(args)
        files.sort()
        expected = '%s/dir1/file1' % directory
        # update directory
        ret = self.plugin.updatedir(files[0], args.dest_dir,
                                    args.FILES[0], args.force)
        # cleanup
        shutil.rmtree(directory)
        return self.assertEqual(ret, expected)

    def test_plugins_local_10_exists(self):
        ''' LOC-10 | local: exists - file exists, return None '''
        filename = 'test/dirtest/file0'
        sys.argv = ['shayfara', '-e', filename]
        args = opts.getopts()
        # test if file already exists
        ret = self.plugin.exists(filename, args)
        return self.assertEqual(ret, None)

    def test_plugins_local_11_exists_force(self):
        ''' LOC-11 | local: exists - file exists, force replace '''
        filename = 'test/dirtest/file0'
        sys.argv = ['shayfara', '-e', '-f', filename]
        args = opts.getopts()
        # test if file already exists
        ret = self.plugin.exists(filename, args)
        return self.assertEqual(ret, filename)

    def test_plugins_local_12_exists(self):
        ''' LOC-12 | local: exists - file does not exist '''
        filename = 'test/dirtest/foo'
        sys.argv = ['shayfara', '-e', filename]
        args = opts.getopts()
        # test if file already exists
        ret = self.plugin.exists(filename, args)
        return self.assertEqual(ret, filename)
