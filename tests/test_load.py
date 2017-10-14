import unittest
from anyloadump import load
import os

class LoadTests(unittest.TestCase):
    def _get_path(self, file):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, file)

    def test_load(self):

        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("anyloadump.loadump").setLevel(logging.DEBUG)
        import json, pickle

        # test text_file(json)
        json_file = self._get_path("data/sample.json")
        res = load.load(json_file)

        with open(json_file, "r") as fi:
            obj = json.load(fi)
        self.assertEqual(res, obj)

        # test binary_file(pickle)
        pickle_file = self._get_path("data/sample.pickle")
        res = load.load(
            filename=pickle_file,
        )

        with open(pickle_file, "rb") as fi:
            obj = pickle.load(fi)

        self.assertEqual(res, obj)

    def test_loads(self):
        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("anyloadump.loadump").setLevel(logging.DEBUG)
        import json, pickle

        sample = [1,2,3]
        s = json.dumps(sample)
        res = load.loads(s, fmt="json") # test
        self.assertEqual(res, sample)

        b = pickle.dumps(sample)
        res = load.loads(b, fmt="pickle")
        self.assertEqual(res, sample)
