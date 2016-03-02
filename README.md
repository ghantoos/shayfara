# shayfara [![Build Status](https://travis-ci.org/ghantoos/shayfara.svg?branch=master)](https://travis-ci.org/ghantoos/shayfara)

## Description

shayfara is a command-line-user-friendly backup encryption tool.

The intend of shayfara is to easy the encryption/decryption of files where you do not have the hand to encrypt the filesystem (e.g. remote storage, the "cloud"). It allows a user to encrypt/decrypt files/directories using ciphering/output plugins.

Available plugins are:

- local (write locally)
- dropbox

See the [plugin section](#plugins) for more information (below).

You can use shayfara to replicate an identical directory-tree and encrypt all the files, making it easy to browse but difficult to see the content. This could be quite useful when saving your pictures on your favorite "cloud" provider, when you are not sure about their privacy engagement (never be sure).

The default cipher uses [simple-crypt](https://github.com/andrewcooke/simple-crypt). It is intented to be slow, in order to prevent attackers from bruteforcing the passphrase. This is because the library is designed to make the key (the password) hard to guess (it uses a PBKDF, which can take a couple of seconds to run). You'll find more information on the [simple-crypt  project page](https://github.com/andrewcooke/simple-crypt#speed).

Files are stored using extensions or can replace the original files. The user-interface was greatly inspired by [lock_files](https://github.com/jlinoff/lock_files)


## Install / Quick test

The default cipher is [simple-crypt](https://github.com/andrewcooke/simple-crypt); it will need to be installed.

```
pip install simple-crypt
cd shayfara
export PYTHONPATH=$PWD
./bin/shayfara
```

Enjoy!

## Standard operations

- To encrypt a file and create a new file:
```
shayfara -e test_images/test.jpg
```

- To encrypt all files in a directory:
```
shayfara -e -v test_images/
```

This will generate file in the same directory adding the ```.enc``` extension (e.g. test.jpg.enc). To overwrite the current file, add ```--in-place```, or change the extension by adding ```--extention 'foo'```


- To encrypt a directory, replicating the directory tree elswhere:
```
shayfara -e -v test_images/ -D /mybackup/directory --in-place

## extended version
shayfara --encrypt --verbose test_images/ --dest-dir /mybackup/directory --in-place
```

- To decrypt, use the same commands as above, replace ```-e|--encrypt``` with ```-d|--decrypt```.


## Plugins
### local
The local plugin is the default plugin. It will write everything locally.

### dropbox
The dropbox plugin will need the dropbox python module as well as an auth token in order to work.

To install the dropbox module: ```pip install dropbox```

You will first need to [create a dropbox app](https://www.dropbox.com/developers/apps/create):

- Choose Dropbox API
- Choose App folder
- Enter an application name

Then go to your app, and [generate a token](https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/).

You can then use shayfara to automatically encrypt and upload your encrypted files to dropbox:
```
shayfara -e test/dirtest/ -O dropbox -v -A '<your_token>'
```

## Global usage

```
usage: shayfara [-h] [-e | -d] [-A AUTH_TOKEN] [-c CIPHER] [-D DEST_DIR]
                [-E EXTENSION] [-f] [-i] [--no-recursive] [-O PLUGIN]
                [-p PASSWORD_FILE | -P PASSWORD] [-v] [-V]
                [FILES [FILES ...]]

shayfara is a user-friendly encryption application

positional arguments:
  FILES                 files to process

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         run in encrypt mode
  -d, --decrypt         run in decrypt mode
  -A AUTH_TOKEN, --auth-token AUTH_TOKEN
                        enter auth token to use with external plugin
  -c CIPHER, --cipher CIPHER
                        select cipher to use (default: simplecrypt)
  -D DEST_DIR, --dest-dir DEST_DIR
                        destination directory (default: same directory)
  -E EXTENSION, --extension EXTENSION
                        add extension the output file names
  -f, --force           force replacing of existing files
  -i, --in-place        use original name - this will replace the original
                        file in case same directory
  --no-recursive        Disable recurse when directories are encountered
                        (default: recursive)
  -O PLUGIN, --plugin PLUGIN
                        select output plugin to use (default: local file)
  -p PASSWORD_FILE, --password-file PASSWORD_FILE
                        file that contains the password (default: prompt user)
  -P PASSWORD, --password PASSWORD
                        password on the command line, not secure (default:
                        prompt user)
  -v, --verbose         level of verbosity
  -V, --version         show program's version number and exit
```
