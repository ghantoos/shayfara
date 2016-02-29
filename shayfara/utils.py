#!/usr/bin/env python3
#
# Copyright (c) 2016, Ignace Mouzannar <ghantoos@ghantoos.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import getpass
import os

from shayfara import msg


def load_files(args):
    '''
    Load the specified files.
    '''
    # init number of errors and file list
    nerrs = 0
    files = []
    for entry in args.FILES:
        # case argument is a file
        if os.path.isfile(entry):
            msg.infov('Loading file ' + entry, args)
            # add to file list and check file access
            files.append(entry)
            nerrs += check_file_access(entry)
        # case argument is a directory and recursive flag
        elif os.path.isdir(entry):
            if args.recursive:
                for wroot, wdirs, wfiles in os.walk(entry):
                    for wfile in sorted(wfiles, key=str.lower):
                        if wfile in ['.', '..']:
                            continue
                        wpath = os.path.join(wroot, wfile)
                        msg.infov('Loading file ' + wpath, args)
                        # add to file list and check file access
                        files.append(wpath)
                        nerrs += check_file_access(wpath)
            else:
                msg.infov('Skipping dir ' + entry, args)
        else:
            msg.errn('Skipping entry %s: No such file or directory' % entry)

    # print total number of loaded files
    msg.infov('%d files loaded' % (len(files)), args)

    # in case errors were found
    if nerrs:
        msg.errx('%d access errors found, cannot proceed' % (nerrs))

    return files


def check_file_access(path):
    '''
    Check the file access.
    '''
    if os.access(path, os.R_OK) is False:
        msg.errn('Cannot read file: %s' % path)
        return 1
    if os.access(path, os.W_OK) is False:
        msg.errn('Cannot write file: %s' % path)
        return 1
    return 0


def get_output_file(ifile, opts):
    '''
    Check that output file does not exist. Skip if exists, unless --force
    is specified.
    '''
    # set file extension depending on en/de-crypt
    if opts.extension:
        ext = '.%s' % opts.extension
    elif opts.extension == '':
        ext = ''
    elif opts.encrypt is True:
        ext = '.enc'
    elif opts.decrypt is True:
        ext = '.dec'

    # concatenate original filename and extension
    ofile = ifile + ext

    return ofile


def get_password(args):
    '''
    Get the password.
    '''
    # User specified it on the command line. Not safe but useful for testing
    # and for scripts.
    if args.password:
        return args.password

    # User specified the password in a file. It should be 0600.
    if args.password_file:
        password = None
        try:
            with open(args.password_file, 'r') as ifp:
                for line in ifp.readlines():
                    line = line.strip()
                    if len(line) == 0:
                        continue  # skip blank lines
                    if line[0] == '#':
                        continue  # skip comments
                    password = line
                    break
        except:
            msg.errx("unable to open password file: %s" % (args.password_file))

        if password is None:
            msg.errx('Password was not found in file %s' % args.password_file)
        return password

    # if password not specify in command-line
    password = getpass.getpass('Password: ')

    # if encryption, ask user to verify password
    if args.encrypt:
        password2 = getpass.getpass('Re-enter password: ')
        if password != password2:
            msg.errx('Passwords did not match!')
    return password
