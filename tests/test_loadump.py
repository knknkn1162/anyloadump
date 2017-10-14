from anyloadump import loadump
import unittest


class LoadumpTests(unittest.TestCase):
    def test_is_binary(self):
        res = loadump._is_binary("./tests/data/sample.json")
        self.assertFalse(res)

        res = loadump._is_binary("./tests/data/sample.pickle")
        self.assertTrue(res)

        # ./data/dummy.pickle: cannot open `./data/dummy.pickle' (No such file or directory)
        self.assertRaises(loadump.CharsetNotInferredError, lambda: loadump._is_binary("./data/dummy.pickle"))

    def test_extract_extension(self):
        res = loadump._extract_extension("./tests/data/sample.json")
        self.assertEqual(res, "json")
        res = loadump._extract_extension("./tests/data/sample.pickle")
        self.assertEqual(res, "pickle")
        self.assertEqual(loadump._extract_extension("./data/dummy"), "")
