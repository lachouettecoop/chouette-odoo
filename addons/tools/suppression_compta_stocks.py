#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Suppression du contenu des tables acount_* et stock_* (en gros)*
"""

import os
import re
import sys
import pdb
import subprocess
import collections
import psycopg2
import psycopg2.extras


def main(args):
    if len(args) < 1:
        print "ERREUR: nom de la base de donnee non specifie"
        sys.exit(-1)
    dbname = args[0]

    if dbname == "db":
        print u"ERREUR: interdit d'effacer la base db"
        sys.exit(-1)

    db=Database(dbname)

    print "Recherche de dépendances"
    dependencies = db.not_null_foreign_key_tables()

    # Ajoute de dépendances à cause d'autres contraintes
    dependencies["account_invoice"].append("account_move")
    dependencies["account_tax"].append("account_account")

    for table in toposort(dependencies):
        if (table.startswith("account_")
                    or table.startswith("stock_")
                    or table.startswith("pos_")
                    or table.startswith("sale_order")
                    or table.startswith("purchase_order")
                    or table.startswith("procurement_order")) \
                and not (table in ("stock_warehouse",
                                   "stock_location",
                                   "pos_category")
                         or table.startswith("pos_config")):
            print "delete from", table
            db.execute("DELETE FROM " + table);


class Database(object):
    def __init__(self, dbname):
        self.db = psycopg2.connect("dbname=" + dbname)
        self.db.autocommit = True
        self.cursor = self.db.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def execute(self, query, args = tuple()):
        sql = self.cursor.mogrify(query, args)
        #print sql
        return self.cursor.execute(sql)

    def fetchall(self):
        return self.cursor.fetchall()

    def public_table_list(self):
        self.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type!='VIEW'
        """)
        return [r[0] for r in self.cursor.fetchall()]

    def table_columns(self, table):
        self.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table,))
        return tuple([r[0] for r in self.cursor.fetchall()])

    def not_null_foreign_key_tables(self):
        """Return the list of tables for which tables has
           a non null foreign key."""
        self.execute("""
            SELECT
                tc.constraint_name, tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                JOIN information_schema.columns AS c
                ON c.column_name = kcu.column_name AND c.table_name=tc.table_name
            WHERE constraint_type = 'FOREIGN KEY' AND is_nullable = 'NO'
        """)
        result = {}
        for r in self.cursor.fetchall():
            table_name, foreign_table_name = r["table_name"], r["foreign_table_name"]
            if foreign_table_name != table_name:
                if not table_name in result: result[table_name] = []
                result[table_name].append(foreign_table_name)
        return result


def toposort(graph):
    """https://gist.github.com/kachayev/5910538
       The MIT License (MIT)
       Copyright (c) 2014 Alexey Kachayev

       Permission is hereby granted, free of charge, to any person obtaining a
       copy of this software and associated documentation
       files (the "Software"), to deal in the Software without restriction,
       including without limitation the rights to use, copy,
       modify, merge, publish, distribute, sublicense, and/or sell copies of the
       Software, and to permit persons to whom the Software
       is furnished to do so, subject to the following conditions:

       The above copyright notice and this permission notice shall be included in
       all copies or substantial portions of the Software.

       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
       IMPLIED, INCLUDING BUT NOT LIMITED TO THE
       WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
       NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
       COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
       WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
       ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
       OTHER DEALINGS IN THE SOFTWARE.
    """
    GRAY, BLACK = 0, 1
    order, enter, state = collections.deque(), set(graph), {}
    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk == BLACK: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK
    while enter: dfs(enter.pop())
    return order


if __name__ == '__main__':
    main(sys.argv[1:])
