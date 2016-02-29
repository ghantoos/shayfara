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

from simplecrypt import encrypt, decrypt, DecryptionException
from shayfara import msg


def encrypt_file(password, ifile):
    with open(ifile, 'rb') as ifp:
        plaintext = ifp.read()
        ciphertext = encrypt(password, plaintext)
        return ciphertext


def decrypt_file(password, ifile):
    try:
        with open(ifile, 'rb') as ifp:
            ciphertext = ifp.read()
            plaintext = decrypt(password, ciphertext)
            return plaintext
    except DecryptionException:
        msg.warn('Bad password or corrupt date, skipping %s'
                 % ifile)
        return None
