import unittest
from anyloadump import dump
import os

class DumpTests(unittest.TestCase):
    def _get_path(self, file):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, file)

    def test_dump(self):
        import json, pickle

        lst = [1,2,3]

        # test json-format
        json_file = self._get_path("data/out.json")
        dump.dump(lst, self._get_path(json_file))
        ## confirm
        with open(json_file, "r") as fi:
            obj = json.load(fi)
        self.assertEqual(lst, obj)

        # test pickle-format
        pickle_file = self._get_path("data/out.pickle")

        dump.dump(lst, self._get_path(pickle_file))
        with open(pickle_file, "rb") as fi:
            obj = pickle.load(fi)
        self.assertEqual(lst, obj)


    def test_dumps(self):
        import json, pickle

        lst = [1,2,3]

        # test json-format
        s = dump.dumps(lst, fmt="json")
        print(s)
        ## confirm
        obj = json.loads(s)
        self.assertEqual(lst, obj)

        # test pickle-format
        s = dump.dumps(lst, "pickle")
        ## confirm
        obj = pickle.loads(s)
        self.assertEqual(lst, obj)

