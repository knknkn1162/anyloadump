from anyloadump import loadump
from anyloadump.loadump import DumpMode
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

    def test_invoke(self):

        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("anyloadump.loadump").setLevel(logging.DEBUG)
        import pickle

        lst = [1,2,3]

        # check if func is json.dump function
        func = loadump._invoke(
            dump_mode=DumpMode.WRITE,
            file = self._get_path("data/sample.json")
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "json")
        self.assertEqual(func.__name__, "dump")

        with open(self._get_path("data/out1.json"), "w") as fo:
            res = func(lst, fo)
        self.assertIsNone(res)

        # check if func is json.load function
        func = loadump._invoke(
            dump_mode=DumpMode.READ,
            file = self._get_path("data/sample.json")
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "json")
        self.assertEqual(func.__name__, "load")

        with open(self._get_path("data/out1.json"), "r") as fi:
            obj = func(fi)
        self.assertEqual(lst, obj)

        # check if func is pickle.load function
        pickle_file = "data/sample.pickle"
        func = loadump._invoke(
            dump_mode=DumpMode.READ,
            file = self._get_path(pickle_file)
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "_pickle")
        self.assertEqual(func.__name__, "load")

        with open(self._get_path(pickle_file), "rb") as fi:
            obj = func(fi)
        with open(self._get_path(pickle_file), "rb") as fi:
            obj_cmp = pickle.load(fi)
        self.assertEqual(obj_cmp, obj)

        # check if func is pickle.dumps function
        func = loadump._invoke(
            dump_mode=DumpMode.WRITE,
            fmt = "pickle"
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "_pickle")
        self.assertEqual(func.__name__, "dumps")

        self.assertEqual(func(lst), pickle.dumps(lst))

        # check if res is pickle.loads function
        func = loadump._invoke(
            dump_mode=DumpMode.READ,
            fmt = "pickle"
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "_pickle")
        self.assertEqual(func.__name__, "loads")


        # check whether ExtensionNotInferredError raises if both file and fmt is None.
        with self.assertRaises(loadump.ExtensionNotInferredError):
            loadump._invoke(
                dump_mode=DumpMode.READ,
            )

    def test_loadump(self):
        # generalized function, tests are described in dump or load module.
        pass
