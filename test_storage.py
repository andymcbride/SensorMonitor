import unittest
from storage import Storage
from pathlib2 import Path


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


if __name__ == '__main__':
    unittest.main()
