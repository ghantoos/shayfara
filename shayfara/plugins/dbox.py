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
import dropbox

from shayfara import msg


class ShayfaraPlugin:

    def __init__(self, auth_token):
        ''' initialize dropbox client connection '''

        self.dboxclient = dropbox.client.DropboxClient(auth_token)

    def write(self, ofile, data):
        ''' write data to local file '''
        try:
            # write temporary local file
            with open(ofile, 'wb') as ofp:
                ofp.write(data)
            # send file to dropbox
            with open(ofile, 'rb') as ofp:
                self.dboxclient.put_file(ofile, ofp)
            # delete temporary local file
            os.remove(ofile)
            return ofile
        except dropbox.rest.ErrorResponse as err:
            msg.errn('Error writing file: %s: %s' % (ofile, err))
            # delete temporary local file
            os.remove(ofile)
            return None

    def remove(self, ofile):
        ''' delete local file '''
        try:
            self.dboxclient.file_delete(ofile)
            return ofile
        except:
            msg.errn('Permission denied: cannot delete file: %s' % ofile)
            return None

    def rename(self, before, after):
        ''' replace original file with generated file '''
        try:
            self.dboxclient.file_move(before, after)
            return after
        except:
            msg.errn('Permission denied: cannot write file: %s' % after)
            return None

    def updatedir(self, ofile, directory, filearg, force=None):
        ''' update file directory, if -D|--directory is specified '''
        # output to specified directory, if -D|--directory
        # replace source dir with dest dir, keeping the dir structure
        sourcedir = os.path.dirname(filearg)
        destdir = os.path.normpath(directory)
        ofile = ofile.replace(sourcedir, destdir, 1)

        return ofile

    def createdir(self, directory):
        ''' create a directory, output error if failed and exit '''
        try:
            self.dboxclient.file_create_folder(directory)
        except:
            msg.errx('Cannot create sub-dir: permission denied: %s'
                     % directory)

    def exists(self, ofile, opts):
        ''' check if file already exists '''
        return ofile
