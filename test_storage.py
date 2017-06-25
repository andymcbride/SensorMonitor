import unittest
from storage import Storage
from pathlib2 import Path
from sqlite3 import IntegrityError


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.db'
        self.storage = Storage(self.filename)

    def tearDown(self):
        path = Path(self.filename)
        path.unlink()

    def test_db_creates(self):
        path = Path(self.filename)
        self.assertEqual(True, path.is_file())

    def test_table_not_exist(self):
        self.assertEqual(False, self.storage.table_exists('data'))

    def test_table_created(self):
        # create table
        self.storage.initialize_tables()
        self.assertEqual(True, self.storage.table_exists('data'))
        self.assertEqual(True, self.storage.table_exists('sensors'))

    def test_create_sensor(self):
        self.storage.initialize_tables()
        self.storage.create_sensor_if_not_exists('Test', 'Temp')

    def test_create_sensor_fail(self):
        self.storage.initialize_tables()
        with self.assertRaises(IntegrityError):
            self.storage.create_sensor_if_not_exists(None, None)

    def test_get_sensor_id(self):
        self.storage.initialize_tables()
        sensor_id = self.storage.create_sensor_if_not_exists('real', 'test')
        self.assertNotEqual(sensor_id, None)
        self.assertEqual(sensor_id, 1)

    def test_get_sensor_id_fail(self):
        self.storage.initialize_tables()
        with self.assertRaises(ValueError):
            sensor_id = self.storage.get_id('FAKE')

    def test_save_sensor_data(self):
        value = {'temperature': 90, 'humidity': 60}
        self.storage.initialize_tables()
        sensor_id = self.storage.create_sensor_if_not_exists('real', 'test')
        self.storage.insert_sensor_data(sensor_id, value)
        result = self.storage.get_latest_value(sensor_id)
        self.assertEqual(value, result)

if __name__ == '__main__':
    unittest.main()
