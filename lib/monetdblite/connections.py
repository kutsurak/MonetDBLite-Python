# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0.  If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 1997 - July 2008 CWI, August 2008 - 2016 MonetDB B.V.

from monetdblite import cursors
from monetdblite import exceptions
from monetdblite import embeddedmonetdb


class Connection(object):
    """A MonetDBLite SQL database connection"""
    def __init__(self, database=None, autocommit=False,
                 hostname=None, username="monetdb", password="monetdb",
                 host=None, user=None, dsn=None):
        """ Initializes the MonetDBLite database.
        args:
            database (str): path to the database directory
            autocommit (bool):  enable/disable auto commit (default: False)

            Ignored Parameters: hostname, username, password, host, user, dsn
        returns:
            Connection object
        """
        global MONETDBLITE_CURRENT_DATABASE
        if database is None:
            if not embeddedmonetdb.is_initialized():
                raise exceptions.ProgrammingError("No database supplied and MonetDBLite was not initialized")
        elif database != embeddedmonetdb.dbpath():
            if embeddedmonetdb.is_initialized():
                raise exceptions.ProgrammingError("MonetDBLite is already initialized. Close the previous connection first.")
            embeddedmonetdb.init(database)
            MONETDBLITE_CURRENT_DATABASE = database

        self.__monetdblite_connection = embeddedmonetdb.connect()
        self.set_autocommit(autocommit)
        self.replysize = 1
        self.__cursors = []

    def close(self):
        for cursor in self.__cursors:
            cursor.close()
        self.__cursors = []
        embeddedmonetdb.shutdown()

    def commit(self):
        # if not embeddedmonetdb.is_initialized():
        #     raise exceptions.Error("This connection has been closed")
        embeddedmonetdb.sql('COMMIT', self.__monetdblite_connection)

    def rollback(self):
        embeddedmonetdb.sql('ROLLBACK', self.__monetdblite_connection)

    def cursor(self):
        cursor = cursors.Cursor(self)
        self.__cursors.append(cursor)
        return cursor

    # MonetDB specific API
    def remove_cursor(self, cursor):
        self.__cursors.remove(cursor)

    def set_autocommit(self, autocommit):
        embeddedmonetdb.set_autocommit(autocommit, self.__monetdblite_connection)
        pass

    def transaction(self):
        embeddedmonetdb.sql('START TRANSACTION', self.__monetdblite_connection)

    def execute(self, query):
        return embeddedmonetdb.sql(query, self.__monetdblite_connection)

    def get_connection(self):
        return self.__monetdblite_connection
