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

import sys


def _msg(prefix, msg, ofp=sys.stdout):
    '''
    Display a simple information message with context information.
    '''
    message = '%s: %s\n' % (prefix, msg)
    ofp.write(message)
    return message


def info(msg, args=None, ofp=sys.stdout):
    '''
    Display a simple information message with context information.
    '''
    message = _msg(prefix='INFO', msg=msg, ofp=ofp)
    return message


def infov(msg, args, ofp=sys.stdout):
    '''
    Display a simple information message with context information.
    '''
    message = ''
    if args.verbose:
        message = _msg(prefix='INFO', msg=msg, ofp=ofp)
    return message


def errx(msg, args=None, ofp=sys.stdout):
    '''
    Display error message with context information and exit.
    '''
    _msg(prefix='ERROR', msg=msg, ofp=ofp)
    sys.exit(1)


def errn(msg, args=None, ofp=sys.stdout):
    '''
    Display error message with context information but do not exit.
    '''
    message = _msg(prefix='ERROR', msg=msg, ofp=ofp)
    return message


def warn(msg, args=None, ofp=sys.stdout):
    '''
    Display error message with context information but do not exit.
    '''
    message = _msg(prefix='WARNING', msg=msg, ofp=ofp)
    return message
