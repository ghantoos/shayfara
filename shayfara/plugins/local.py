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
from shayfara.plugins import ShayfaraPlugin


class PluginLocal(ShayfaraPlugin):

    def write(self, ofile, data, ifile):
        ''' write data to local file '''
        try:
            # get original file system status using stat(1)
            stat = os.stat(ifile)
            # write file to disk
            with open(ofile, 'wb') as ofp:
                ofp.write(data)
            # restore original file system status
            os.chmod(ofile, stat.st_mode)
            return ofile
        except:
            msg.errn('Error occured while writing file: %s' % ofile)
            return None

    def remove(self, ofile):
        ''' delete local file '''
        try:
            os.remove(ofile)
            return ofile
        except:
            msg.errn('Permission denied: cannot delete file: %s' % ofile)
            return None

    def rename(self, before, after):
        ''' replace original file with generated file '''
        try:
            os.rename(before, after)
            return after
        except:
            msg.errn('Permission denied: cannot write file: %s' % after)
            return None

    def createdir(self, directory):
        ''' create a directory, output error if failed and exit '''
        if not os.path.isdir(directory):
            try:
                msg.info('Creating directory: %s' % directory)
                os.makedirs(directory)
            except:
                msg.errx('Cannot create sub-dir: permission denied: %s'
                         % directory)

    def exists(self, ofile, opts):
        ''' check if file already exists '''
        # in case file already exists, skip
        if os.path.isfile(ofile) and opts.force is False:
            msg.errn('Already exists, skipping: %s' % ofile)
            ofile = None
        return ofile
