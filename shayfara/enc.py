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


def crypt(args):
    '''
    Encrypt or decrypt the files.
    '''
    # set mode, used by messages (msg.py)
    if args.decrypt is True:
        mode = 'decrypt'
    else:
        mode = 'encrypt'

    # init return code
    ret = 0
    skipped = 0

    # set cipher to use
    if args.cipher == 'simplecrypt':
        from shayfara.ciphers import scrypt
        cipher = scrypt

    # set output plug-in to use
    if args.plugin == 'local':
        from shayfara.plugins import local
        plugin = local.PluginLocal()
    elif args.plugin == 'dropbox':
        from shayfara.plugins import dbox
        if args.auth_token:
            plugin = dbox.PluginDropbox(args.auth_token)
        else:
            msg.errx('Authentification token required for dropbox plugin')

    # get password
    password = utils.get_password(args)

    # expand all files from command line
    files = utils.load_files(args)

    # parse and process files
    for ifile in files:
        # get output file name
        # returns empty if file exists and --force not specified
        ofile = utils.get_output_file(ifile, args)

        # in case new directory is specified using -D|--dest-dir
        # create directory in --force, skip if dry-run
        if args.force is True and args.dry_run is False:
            plugin.createdir(args.dest_dir)
        # update output file path
        if args.dest_dir:
            ofile = utils.updatedir(ofile, args.dest_dir, args.FILES[0])

        # check if files exists, and force is not specified
        ofile = plugin.exists(ofile, args)

        # if output file name is empty, skip file
        if ofile is None:
            skipped += 1
            continue

        # write action (encrypting/decrypting) if verbose
        msg.infov('%sing: %s' % (mode, ofile), args=args)

        if args.decrypt:
            # encrypt file using extension
            output = cipher.decrypt_file(password, ifile)
        else:
            # encrypt file using extension
            output = cipher.encrypt_file(password, ifile)

        # write output using proper plug-in
        # if out is empty, increment error
        if output:
            # skip if dry-run
            if args.dry_run is False:
                # write to file, increment skipped if error occurs
                if not plugin.write(ofile, output):
                    skipped += 1
                    continue
        else:
            skipped += 1
            continue

        # in case --in-place, rename file to original (replace)
        if args.in_place and args.dest_dir is None:
            msg.infov('renaming  : %s' % ifile, args)
            # skip if dry-run
            if args.dry_run is False:
                # if out is empty, increment error
                if plugin.rename(ofile, ifile):
                    ret += 1
                    continue

    if args.dry_run is False:
        msg.info('%d files %sed' % (len(files) - skipped, mode), args=args)
    else:
        msg.info('%d files %sed (DRY RUN)'
                 % (len(files) - skipped, mode), args=args)

    return ret
