import os
import unittest
import uuid

from src import common


class MyTestCase(unittest.TestCase):

    def test_logger(self):
        file_name = str(uuid.uuid4())
        logger = common.Logger(log_file_name=file_name, log_mode='a')
        logger.log_message('TRACKS', 'Hello')
        logger.log_message('Client', 'Hello Tracks')

        with open(os.path.join(os.path.join(common.project_root(), 'logs'), file_name + '.log')) as f:
            f = f.readlines()
            self.assertEqual(True, 'TRACKS' in f[0])
            self.assertEqual(True, 'Client' in f[1])
            self.assertEqual(True, 'TRACKS' not in f[1])
            self.assertEqual(True, 'Tracks' in f[1])


if __name__ == '__main__':
    unittest.main()
