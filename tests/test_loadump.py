from anyloadump import loadump
import unittest
import os
import logging

logger = logging.getLogger(__name__)


class LoadumpTests(unittest.TestCase):
    def _get_path(self, file):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, file)

    def test_is_binary(self):
        import logging
        logging.basicConfig(level=logging.ERROR)

        for module in ["anyloadump.loadump", "tests.test_loadump"]:
            logging.getLogger(module).setLevel(logging.DEBUG)

        res = loadump._is_binary(self._get_path("data/sample.json"))
        self.assertFalse(res)

        res = loadump._is_binary(self._get_path("data/sample.pickle"))
        self.assertTrue(res)

        with self.assertRaises(FileNotFoundError):
            loadump._is_binary(self._get_path("data/dummy.pickle"))


    def test_extract_extension(self):
        res = loadump._extract_extension(self._get_path("data/sample.json"))
        self.assertEqual(res, "json")
        res = loadump._extract_extension(self._get_path("data/sample.pickle"))
        self.assertEqual(res, "pickle")
        self.assertEqual(loadump._extract_extension(self._get_path("data/dummy")), "")
