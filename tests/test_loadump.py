from anyloadump import loadump
import unittest
import os


class LoadumpTests(unittest.TestCase):
    def _get_path(self, file):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, file)

    def test_is_binary(self):
        import logging
        logging.basicConfig(level=logging.ERROR)

        logging.getLogger("anyloadump.loadump").setLevel(logging.DEBUG)

        res = loadump._is_binary(self._get_path("data/sample.json"))
        self.assertFalse(res)

        res = loadump._is_binary(self._get_path("data/sample.pickle"))
        self.assertTrue(res)

        # ./data/dummy.pickle: cannot open `./data/dummy.pickle' (No such file or directory)
        self.assertRaises(
            loadump.CharsetNotInferredError,
            lambda: loadump._is_binary(self._get_path("data/dummy.pickle"))
        )

    def test_extract_extension(self):
        res = loadump._extract_extension(self._get_path("data/sample.json"))
        self.assertEqual(res, "json")
        res = loadump._extract_extension(self._get_path("data/sample.pickle"))
        self.assertEqual(res, "pickle")
        self.assertEqual(loadump._extract_extension(self._get_path("data/dummy")), "")
