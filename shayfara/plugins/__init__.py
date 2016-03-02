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

from shayfara import msg


class ShayfaraPlugin:
    ''' Plugin template that is followed by all the shayfara plug-ins '''

    def __init__(self):
        ''' initialize local plug-in '''
        pass

    def write(self, ofile, data):
        ''' write data to local file
            - return 'ofile' if write successful
            - return None if failed
        '''
        return None

    def remove(self, ofile):
        ''' delete local file
            - return 'ofile' if write successful
            - return None if failed
        '''
        return None

    def rename(self, before, after):
        ''' replace original file with generated file
            - return 'after' if write successful
            - return None if failed
        '''
        return None

    def updatedir(self, ofile, directory, filearg, force=None):
        ''' update file directory, if -D|--directory is specified
            - return 'ofile' if write successful
            - exit using msg.errx() if failed
        '''
        msg.errx('You should not be seing this message: %s' % directory)

    def createdir(self, directory):
        ''' create a directory, output error if failed and exit
            - return 'ofile' if write successful
            - exit using msg.errx() if failed
        '''
        msg.errx('You should not be seing this message: %s' % directory)

    def exists(self, ofile, opts):
        ''' check if file already exists
            - return 'after' if write successful
            - return None if failed
        '''
        return None
