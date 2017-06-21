import sqlite3


class Storage(object):

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)

    def table_exists(self,table):
        stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        c = self.conn.cursor()
        params = (table,)
        c.execute(stmt, params)
        result = c.fetchone()
        if result is not None and table in result:
            return True
        return False

    def initialize_tables(self):
        self._create_table("CREATE TABLE data (id INT PRIMARY KEY NOT NULL, sensor_id INT NOT NULL, value DECIMAL(5,2) NOT NULL, timestamp DATE DEFAULT (datetime('now','localtime')))")
        self._create_table("CREATE TABLE sensors (id INT PRIMARY KEY NOT NULL, name VARCHAR(80) NOT NULL, type VARCHAR(80) NOT NULL)")

    def _create_table(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Exception as e:
            print(e)


