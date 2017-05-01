#!/usr/bin/env python

"""
Try to dump Odoo database in a way suitable for diff
after updating Odoo (openerp-server -d db -u all)
"""

import psycopg2


db = psycopg2.connect("dbname=db")
cursor = db.cursor()


EXCLUDE_TABLES = ("ir_module_module", "ir_model_fields", "ir_model_fields_group_rel" ,"ir_module_module_dependency")
EXCLUDE_COLUMNS = ("create_uid", "create_date", "write_uid", "write_date", "date_init", "date_update", "model_data_id")

ORDER_BY_TABLE = {
    "ir_act_window_view": ["view_id", "act_window_id", "id"],
    "ir_model_data": ["module", "model", "name"],
    "ir_ui_menu_group_rel": ["menu_id", "gid"],
    "ir_ui_view_group_rel": ["view_id", "group_id"],
    "ir_values": ["model", "name"],
    "account_fiscal_position_tax_template": ["tax_src_id", "tax_dest_id"],
}

def public_table_list():
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type!='VIEW'
    """)
    return [r[0] for r in cursor.fetchall() if r[0] not in EXCLUDE_TABLES]

def table_columns(table):
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
    """, (table,))
    return [r[0] for r in cursor.fetchall() if not r[0] in EXCLUDE_COLUMNS]


def to_string(table, column, value):
    res = str(value)
    if table=="ir_attachment" and column =="index_content":
        res = res.replace("(u'image',)", "image")
    if res.endswith(".0"):
        res = res[:-2]
    return res

for table in sorted(public_table_list()):
    columns = table_columns(table)
    columns_order = ORDER_BY_TABLE[table] if table in ORDER_BY_TABLE else ["id"] if "id" in columns else []
    if len(columns_order) > 0:
        order = "ORDER BY " + ", ".join(columns_order)
        columns = columns_order + [c for c in columns if not c in columns_order]
    else:
        order = ""
    row_where = []
    if table=="ir_translation":
        row_where.append("value != src")
    where = "WHERE " + " AND ".join(row_where) if len(row_where)>0 else ""

    cursor.execute('SELECT "{0}" FROM {1} {2} {3}'.format(
        '","'.join(columns), table, where, order))

    print
    print "|===================================================|"
    print "|", table, "|"
    print "|===================================================|"
    print "  |  ".join(columns)
    for r in cursor.fetchall():
        s = ""
        for i in range(len(columns)):
            if i>0:
                s = s + "  |  "
            s = s + to_string(table, columns[i], r[i])
        print s
