import unittest
from anyloadump import dump
import os

class DumpTests(unittest.TestCase):
    def _get_path(self, file):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, file)

    def test_dump(self):
        self.assertTrue(False)

    def test_dumps(self):
        self.assertTrue(False)

