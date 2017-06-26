import sqlite3
import json
from sensor import SensorData


class Storage(object):

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)

    def create_sensor_if_not_exists(self, name, sensor_type):
        try:
            c = self.conn.cursor()
            try:
                sensor_id = self.get_id('name')
                if sensor_id is not None:
                    return sensor_id
            except:
                pass
            c.execute("insert into sensors(name, type) values(?, ?)", (name, sensor_type))
            self.conn.commit()
            if c.rowcount is not 1:
                raise IOError("Unable to create sensor")
            return c.lastrowid
        except:
            raise

    def get_id(self, name):
        c = self.conn.cursor()
        c.execute("select id from sensors where name = ?", (name,))
        row = c.fetchone()
        if row is None:
            raise ValueError('No such sensor found')
        return row[0]

    def insert_sensor_data(self, sensor_data):
        json_value = json.dumps(sensor_data.get_values())
        c = self.conn.cursor()
        c.execute("insert into data(sensor_id, value) VALUES (?, ?)", (sensor_data.sensor_id, json_value))
        self.conn.commit()

    def get_latest_value(self, sensor_id):
        c = self.conn.cursor()
        c.execute("select value from data where sensor_id = ? order by timestamp DESC limit 1", (sensor_id,))
        row = c.fetchone()
        if row is None:
            raise ValueError("No data for sensor id: {}".format(sensor_id))
        return json.loads(row[0])

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


