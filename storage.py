import sqlite3


class Storage(object):

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)

    def create_sensor(self, name, sensor_type):
        try:
            c = self.conn.cursor()
            c.execute("insert into sensors(name, type) values(?, ?)", (name, sensor_type))
            self.conn.commit()
            if c.rowcount is not 1:
                raise IOError("Unable to create sensor")
        except:
            raise

    def get_id(self, name):
        c = self.conn.cursor()
        c.execute("select id from sensors where name = ?", (name,))
        row = c.fetchone()
        if row is None:
            raise ValueError('No such sensor found')
        return row[0]

    def insert_sensor_data(self, sensor_id, value):
        pass

    def table_exists(self,table):
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        result = c.fetchone()
        if result is not None and table in result:
            return True
        return False

    def initialize_tables(self):
        self._create_table("CREATE TABLE data (id INTEGER PRIMARY KEY, sensor_id INT NOT NULL, value TEXT NOT NULL, timestamp DATE DEFAULT (datetime('now','localtime')))")
        self._create_table("CREATE TABLE sensors (id INTEGER PRIMARY KEY, name VARCHAR(80) NOT NULL, type VARCHAR(80) NOT NULL)")

    def _create_table(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Exception as e:
            print(e)


