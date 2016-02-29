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
from shayfara import utils


def crypt(opts, password, files):
    '''
    Encrypt or decrypt the files.
    '''
    # set mode, used by messages (msg.py)
    if opts.decrypt is True:
        mode = 'decrypt'
    else:
        mode = 'encrypt'

    # init return code
    ret = 0
    skipped = 0

    # set cipher to use
    if opts.cipher == 'simplecrypt':
        from shayfara.ciphers import scrypt
        cipher = scrypt

    # set output plug-in to use
    if opts.plugin == 'local':
        from shayfara.plugins import local
        plugin = local

    # parse and process files
    for ifile in files:
        # get output file name
        # returns empty if file exists and --force not specified
        ofile = utils.get_output_file(ifile, opts)

        # in case new directory is specified using -D|--directory
        if opts.directory:
            ofile = plugin.updatedir(ofile, opts.directory, opts.FILES[0])

        # check if files exists, and force is not specified
        ofile = plugin.exists(ofile, opts)

        # if output file name is empty, skip file
        if ofile is None:
            skipped += 1
            continue

        msg.infov('%s %s' % (mode, ofile), args=opts)

        if opts.decrypt:
            # encrypt file using extension
            output = cipher.decrypt_file(password, ifile)
        else:
            # encrypt file using extension
            output = cipher.encrypt_file(password, ifile)

        # write output using proper plug-in
        # if out is empty, increment error
        if output:
            if not plugin.write(ofile, output):
                skipped += 1
                continue
        else:
            skipped += 1
            continue

        # in case --inplace, rename file to original (replace)
        if opts.inplace:
            # if out is empty, increment error
            if plugin.rename(ofile, ifile):
                ret += 1
                continue

    msg.infov('%d files %sed' % (len(files) - skipped, mode), args=opts)

    return ret
