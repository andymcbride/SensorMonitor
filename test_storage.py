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
        self.storage.create_sensor('Test', 'Temp')

    def test_create_sensor_fail(self):
        self.storage.initialize_tables()
        with self.assertRaises(IntegrityError):
            self.storage.create_sensor(None, None)

    def test_get_sensor_id(self):
        self.storage.initialize_tables()
        self.storage.create_sensor('real', 'test')
        row_id = self.storage.get_id('real')
        self.assertNotEqual(row_id, None)
        self.assertEqual(row_id, 1)

    def test_get_sensor_id_fail(self):
        self.storage.initialize_tables()
        with self.assertRaises(ValueError):
            id = self.storage.get_id('FAKE')


if __name__ == '__main__':
    unittest.main()
