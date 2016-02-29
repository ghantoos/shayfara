import unittest
import sys
import os
import tempfile

from shayfara import opts
from shayfara import utils
from shayfara.ciphers import scrypt


class TestFunctions(unittest.TestCase):

    def test_ciphers_01_scrypt_encrypt(self):
        ''' CIP-01 | scrypt: encrypt file '''
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'Some data')
            filename = f.name
        sys.argv = ['shayfara', '-e', '-p', 'test/passwordfile', filename]
        args = opts.getopts()
        expected = 'Some data'
        # get password
        password = utils.get_password(args)
        # encrypt data read from file
        ret = scrypt.encrypt_file(password, filename)
        os.remove(filename)
        return self.assertNotEqual(ret, expected)

    def test_ciphers_02_scrypt_decrypt_success(self):
        ''' CIP-02 | scrypt: encrypt then decrypt file '''
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'Some data')
            inputfile = f.name
        sys.argv = ['shayfara', '-e', '-p', 'test/passwordfile', inputfile]
        args = opts.getopts()
        expected = b'Some data'
        # get password
        password = utils.get_password(args)
        # encrypt data read from file
        ret = scrypt.encrypt_file(password, inputfile)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(ret)
            encfile = f.name
        # decrypt data from above encrypted file
        ret = scrypt.decrypt_file(password, encfile)
        os.remove(inputfile)
        os.remove(encfile)
        return self.assertEqual(ret, expected)

    def test_ciphers_03_scrypt_decrypt_failure(self):
        ''' CIP-03 | scrypt: encrypt then fail decrypt file
            (bad password)
        '''
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'Some data')
            inputfile = f.name
        sys.argv = ['shayfara', '-e', '-p', 'test/passwordfile', inputfile]
        args = opts.getopts()
        expected = None
        # get password
        password = utils.get_password(args)
        # encrypt data read from file
        ret = scrypt.encrypt_file(password, inputfile)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(ret)
            encfile = f.name
        # decrypt data from above encrypted file
        ret = scrypt.decrypt_file('badpassword', encfile)
        os.remove(inputfile)
        os.remove(encfile)
        return self.assertEqual(ret, expected)
