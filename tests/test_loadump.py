from anyloadump import loadump
import unittest


class LoadumpTests(unittest.TestCase):
    def test_is_binary(self):
        res = loadump._is_binary("./data/sample.json")
        self.assertFalse(res)

        res = loadump._is_binary("./data/sample.pickle")
        self.assertTrue(res)

        # ./data/dummy.pickle: cannot open `./data/dummy.pickle' (No such file or directory)
        self.assertRaises(loadump.CharsetNotInferredError, lambda: loadump._is_binary("./data/dummy.pickle"))
