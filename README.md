shayfara [![Build Status](https://travis-ci.org/ghantoos/shayfara.svg?branch=master)](https://travis-ci.org/ghantoos/shayfara)
========


shayfara is a command-line-user-friendly backup encryption tool.

The intend of shayfara is to easy the encryption/decryption of files where you do not have the hand to encrypt the filesystem (e.g. remote storage, the "cloud"). It allows a user to encrypt/decrypt files/directories using ciphering/output plugins.

The default cipher uses [simple-crypt](https://github.com/andrewcooke/simple-crypt). It is intented to be slow, in order to prevent attackers from bruteforcing the passphrase. This is because the library is designed to make the key (the password) hard to guess (it uses a PBKDF, which can take a couple of seconds to run). You'll find more information on the [simple-crypt  project page](https://github.com/andrewcooke/simple-crypt#speed).

Files are stored using extensions or can replace the original files. The user-interface was greatly inspired by [lock_files](https://github.com/jlinoff/lock_files)


Install / Quick test:
---------------------

The default cipher is [simple-crypt](https://github.com/andrewcooke/simple-crypt); it will need to be installed.

```
pip install simple-crypt
cd shayfara
export PYTHONPATH=$PWD
./bin/shayfara
```

Enjoy!

Standard operations:
--------------------

- To encrypt a file and create a new file:
```
shayfara -e test_images/test.jpg
```

- To encrypt a file overwriting the original file:
```
shayfara -e -v --inplace test_images/test.jpg
```

- To encrypt a directory, add ```--recursive|-r``` flag:
```
shayfara -e -v -r test_images/ -D /mybackup/directory -x ''

## extended version
shayfara --encrypt --verbose --recursive test_images/ --dest-dir /mybackup/directory --extension ''
```

- To decrypt a file and create a new file:
```
shayfara -d test.jpg.enc -v
```

- To decrypt a directory:
```
shayfara -d -v -r /mybackup/directory -D /not/encrypted/dir -x ''

## extended verion
shayfara --decrypt --verbose --recursive /mybackup/directory --dest-dir /not/encrypted/dir --extension ''
```

Global usage:
-------------

```
usage: shayfara [-h] [-d | -e] [-p PASSWORD_FILE | -P PASSWORD] [-r]
                [-x EXTENSION] [-i] [-f] [-c CIPHER] [-o OUTPUT] [-v] [-V]
                [FILES [FILES ...]]

shayfara is a user-friendly encryption application

positional arguments:
  FILES                 files to process

optional arguments:
  -h, --help            show this help message and exit
  -d, --decrypt         decrypt
  -e, --encrypt         encrypt
  -p PASSWORD_FILE, --password-file PASSWORD_FILE
                        file that contains the password, default is to prompt
  -P PASSWORD, --password PASSWORD
                        password on the command line, not secure
  -r, --recurse         recurse when directories are encountered
  -x EXTENSION, --extension EXTENSION
                        add extension the output file names
  -i, --inplace         rename file to original name (replace)
  -f, --force           force replacing of existing files
  -c CIPHER, --cipher CIPHER
                        select cipher to use. Default: simplecrypt
  -o OUTPUT, --output OUTPUT
                        select output plugin to use. Default: local file
  -v, --verbose         level of verbosity
  -V, --version         show program's version number and exit
```
