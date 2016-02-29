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

import os

from shayfara import msg


def write(ofile, data):
    ''' write data to local file '''
    try:
        with open(ofile, 'wb') as ofp:
            ofp.write(data)
        return ofile
    except:
        msg.errn('Error occured while writing file: %s' % ofile)
        return None


def remove(ofile):
    ''' delete local file '''
    try:
        os.remove(ofile)
        return ofile
    except:
        msg.errn('Permission denied: cannot delete file: %s' % ofile)
        return None


def rename(before, after):
    ''' replace original file with generated file '''
    try:
        os.rename(before, after)
        return after
    except:
        msg.errn('Permission denied: cannot write file: %s' % after)
        return None


def updatedir(ofile, directory, filearg, force=None):
    ''' update file directory, if -D|--directory is specified '''
    # force creation of target directory, if it does not exist and --force
    if not os.path.isdir(directory) and force:
        msg.info('Creating directory: %s' % directory)
        createdir(directory)

    # output to specified directory, if -D|--directory
    if os.path.isdir(directory):
        # replace source dir with dest dir, keeping the dir structure
        sourcedir = os.path.dirname(filearg)
        destdir = os.path.normpath(directory)
        ofile = ofile.replace(sourcedir, destdir, 1)
        odir = os.path.dirname(ofile)
        # create destination directory if not existing
        createdir(odir)
    else:
        msg.errx('No such directory: %s' % directory)

    return ofile


def createdir(directory):
    ''' tre creating a directory, output error if failed '''
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except:
            msg.errx('Cannot create sub-dir: permission denied: %s'
                     % directory)


def exists(ofile, opts):
    ''' check if file already exists '''
    # in case file already exists, skip
    if os.path.isfile(ofile) and opts.force is False:
        msg.errn('Already exists, skipping: %s' % ofile)
        ofile = None
    return ofile
