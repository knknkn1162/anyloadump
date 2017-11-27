import unittest
import anyloadump as ald
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
        ald.dump(lst, self._get_path(json_file))
        ## confirm
        with open(json_file, "r") as fi:
            obj = json.load(fi)
        self.assertEqual(lst, obj)

        # test pickle-format
        pickle_file = self._get_path("data/out.pickle")

        ald.dump(lst, self._get_path(pickle_file))
        with open(pickle_file, "rb") as fi:
            obj = pickle.load(fi)
        self.assertEqual(lst, obj)


    def test_dumps(self):
        import json, pickle

        lst = [1,2,3]

        # test json-format
        s = ald.dumps(lst, fmt="json")
        ## confirm
        obj = json.loads(s)
        self.assertEqual(lst, obj)

        # test pickle-format
        s = ald.dumps(lst, "pickle")
        ## confirm
        obj = pickle.loads(s)
        self.assertEqual(lst, obj)


    ## -----almost same as dump.dump method except for open_mode -----#
    def test_xdump(self):
        pass

    def test_adump(self):
        pass

    ## ------almost same as dump.dumps method except for open_mode -----#
    def test_xdumps(self):
        pass

    def test_adumps(self):
        pass


class NonExistendPathDumpTests(unittest.TestCase):
    def test_dump_directory_is_notfound_when_created(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            storedir = os.path.join(tmpdir, "store")
            self.assertFalse(os.path.exists(storedir))

            data = {"x": 1}
            ald.dump(data, os.path.join(storedir, "data.json"))

            self.assertTrue(os.path.exists(storedir))
            loaded = ald.load(os.path.join(storedir, "data.json"))
            self.assertEqual(data, loaded)
