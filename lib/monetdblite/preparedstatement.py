# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0.  If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 1997 - July 2008 CWI, August 2008 - 2018 MonetDB B.V.

from monetdblite import monetize
from monetdblite import embeddedmonetdb


class PreparedStatement:
    def __init__(self, stmt_id, client, type_array, query_text):
        self._stmt_id = stmt_id
        self._client = client
        self._parameter_type_array = type_array
        self._query_text = query_text

    def __str__(self):
        tmpstr = ""
        for tp in self._parameter_type_array:
            tmpstr += "  {} {}\n".format(tp['sql_type_name'], tp['digits'])
        retval = "Statement id: {}\nQuery:\n  {}\nParameter types:\n{}".format(self._stmt_id, self._query_text, tmpstr)
        return retval

    def execute(self, *args):
        monetized_args = [monetize.convert(x) for x in args]
        monetized_args_list = ",".join(monetized_args)
        # TODO: make sure this is what we need to be doing.
        exec_string = "execute {}({})".format(self._stmt_id, monetized_args_list)

        return embeddedmonetdb.sql(exec_string)

    def release():
        pass
