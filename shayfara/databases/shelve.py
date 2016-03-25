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

import shelve
import os

from shayfara.databases import ShayfaraDB


class DBShelve(ShayfaraDB):
    ''' This class will initialize the shayfara database and present a set
        of functions to add/remove/update entries
    '''

    def __init__(self, dbdir, db='.shayfara'):
        ''' initialize the database '''
        database = os.path.join(dbdir, db)
        self._db = self.open(database)

    def open(self, dbname):
        ''' create the database to be used by shayfara '''
        return shelve.open(dbname, 'c')

    def close(self):
        return self._db.close()

    def put(self, key, value):
        self._db[key] = value

    def get(self, key):
        print(self._db.get(key))

    def has(self, key):
        """Determines whether a key exists within the database"""
        return key in self._db.keys()

    def delete(self, key):
        if self.has(key):
            del self._db[key]
            return True
