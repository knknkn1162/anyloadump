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

        # for travis ci
        import subprocess
        try:
            subprocess.run(["file", "--mime", "."], stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as err:
            logger.debug("{}".format(err))
            return

        res = loadump._is_binary(self._get_path("data/sample.json"))
        self.assertFalse(res)

        res = loadump._is_binary(self._get_path("data/sample.pickle"))
        self.assertTrue(res)

        # ./data/dummy.pickle: cannot open `./data/dummy.pickle' (No such file or directory)
        with self.assertRaises(loadump.CharsetNotInferredError):
            loadump._is_binary(self._get_path("data/dummy.pickle"))


    def test_extract_extension(self):
        res = loadump._extract_extension(self._get_path("data/sample.json"))
        self.assertEqual(res, "json")
        res = loadump._extract_extension(self._get_path("data/sample.pickle"))
        self.assertEqual(res, "pickle")
        self.assertEqual(loadump._extract_extension(self._get_path("data/dummy")), "")
