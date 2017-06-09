import unittest
from storage import Storage
from pathlib2 import Path


class MyTestCase(unittest.TestCase):

    def test_db_creates(self):
        file = 'test.db'
        storage = Storage(file=file)
        path = Path(file)
        self.assertEqual(True, path.is_file())
        path.unlink()

    def test_table_not_exist(self):
        file = 'test.db'
        table = 'sensors'
        storage = Storage(file=file, table=table)
        path = Path(file)
        self.assertEqual(False, storage.table_exists())
        path.unlink()

    def test_table_created(self):
        file = 'test.db'
        table = 'sensors'
        storage = Storage(file=file, table=table)
        path = Path(file)
        # create table

        path.unlink()





if __name__ == '__main__':
    unittest.main()
