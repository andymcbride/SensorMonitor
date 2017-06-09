import sqlite3


class Storage(object):

    def __init__(self, file='data.db', table='sensors'):
        self.file = file
        self.table = table

        conn = sqlite3.connect(file)
        self.dbc = conn.cursor()

    def table_exists(self):
        stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        params = (self.table,)
        self.dbc.execute(stmt, params)
        if self.dbc.rowcount != -1:
            return True
        return False

    def initialize_table(self):
        stmt = "CREATE TABLE %s(id INTEGER PRIMARY KEY ASC, sensor_id, value_type, value, time)"
        params = (self.table, )


