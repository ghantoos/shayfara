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

import argparse

from shayfara import variables


def getopts(arg=None):
    '''
    Get the command line options.
    '''
    description = 'shayfara is a user-friendly encryption application'
    rawd = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=rawd,
                                     description=description,
                                     prefix_chars='-')

    # group1: encrypt or decrypt
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-e', '--encrypt',
                        action='store_true',
                        help='run in encrypt mode')

    group1.add_argument('-d', '--decrypt',
                        action='store_true',
                        help='run in decrypt mode')

    # group2: provide password file or command-line
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-p', '--password-file',
                        action='store',
                        type=str,
                        help='file that contains the password '
                             '(default: prompt user)')

    group2.add_argument('-P', '--password',
                        action='store',
                        type=str,
                        help='password on the command line, not secure '
                             '(default: prompt user)')

    # other flags
    parser.add_argument('--no-recursive',
                        action='store_false',
                        default=True,
                        help='Disable recurse when directories are encountered'
                             ' (default: recursive)')

    parser.add_argument('-x', '--extension',
                        action='store',
                        help='add extension the output file names')

    parser.add_argument('-i', '--inplace',
                        action='store_true',
                        help='rename file to original name (replace)')

    parser.add_argument('-D', '--dest-dir',
                        action='store',
                        help='destination directory (default: same directory)')

    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='force replacing of existing files')

    parser.add_argument('-c', '--cipher',
                        action='store',
                        default='simplecrypt',
                        help='select cipher to use (default: simplecrypt)')

    parser.add_argument('-O', '--plugin',
                        action='store',
                        default='local',
                        help='select output plugin to use '
                             '(default: local file)')

    parser.add_argument('-v', '--verbose',
                        action='count',
                        help='level of verbosity')

    parser.add_argument('-V', '--version',
                        action='version',
                        version='shayfara - version %s'
                                % variables.__version__)

    parser.add_argument('FILES',
                        nargs="*",
                        help='files to process')

    # print help menu
    if arg == ['help']:
        ret = parser.parse_args(['--help'])
    else:
        ret = parser.parse_args()

    return ret
