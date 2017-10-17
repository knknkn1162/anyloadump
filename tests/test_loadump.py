from anyloadump import loadump
from anyloadump.loadump import Loadumper, OpenMode
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

        ld = Loadumper()
        res = ld._is_binary(self._get_path("data/sample.json"))
        self.assertFalse(res)

        res = ld._is_binary(self._get_path("data/sample.pickle"))
        self.assertTrue(res)

        res = ld._is_binary(self._get_path("data/dummy.pickle"))
        self.assertTrue(res)

        # assume that tb_mapping doesn't support json or pickle.
        ld = Loadumper({"json": None, "pickle": None})
        res = ld._is_binary(self._get_path("data/sample.json"))
        self.assertFalse(res)

        res = ld._is_binary(self._get_path("data/sample.pickle"))
        self.assertTrue(res)

        res = ld._is_binary(self._get_path("data/dummy.pickle"))
        self.assertTrue(res)

        import sys
        # ModuleNotFoundError is new in python3.6. otherwise assume to be raised ImportError
        with self.assertRaises(ModuleNotFoundError if sys.version_info.minor>=6 else ImportError):
            ld._is_binary(self._get_path("data/dummy.dummy"))

        with self.assertRaises(loadump.CharsetNotInferredError):
            ld._is_binary(self._get_path("data/dummy.os"))


    def test_extract_extension(self):
        res = Loadumper._extract_extension(self._get_path("data/sample.json"))
        self.assertEqual(res, "json")
        res = Loadumper._extract_extension(self._get_path("data/sample.pickle"))
        self.assertEqual(res, "pickle")
        self.assertEqual(Loadumper._extract_extension(self._get_path("data/dummy")), "")

    def test_invoke(self):

        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("anyloadump.loadump").setLevel(logging.DEBUG)
        import pickle

        lst = [1,2,3]

        # check if func is json.dump function
        func = Loadumper._invoke(
            open_mode=OpenMode.WRITE,
            filename = self._get_path("data/sample.json")
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "json")
        self.assertEqual(func.__name__, "dump")

        with open(self._get_path("data/out1.json"), "w") as fo:
            res = func(lst, fo)
        self.assertIsNone(res)

        # check if func is json.load function
        func = Loadumper._invoke(
            open_mode=OpenMode.READ,
            filename = self._get_path("data/sample.json")
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "json")
        self.assertEqual(func.__name__, "load")

        with open(self._get_path("data/out1.json"), "r") as fi:
            obj = func(fi)
        self.assertEqual(lst, obj)

        # check if func is pickle.load function
        pickle_file = "data/sample.pickle"
        func = Loadumper._invoke(
            open_mode=OpenMode.READ,
            filename = self._get_path(pickle_file)
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
        func = Loadumper._invoke(
            open_mode=OpenMode.WRITE,
            fmt = "pickle"
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "_pickle")
        self.assertEqual(func.__name__, "dumps")

        self.assertEqual(func(lst), pickle.dumps(lst))

        # check if res is pickle.loads function
        func = Loadumper._invoke(
            open_mode=OpenMode.READ,
            fmt = "pickle"
        )
        self.assertTrue(hasattr(func, '__call__'))
        self.assertEqual(func.__module__, "_pickle")
        self.assertEqual(func.__name__, "loads")


        # check whether ExtensionNotInferredError raises if both file and fmt is None.
        with self.assertRaises(loadump.ExtensionNotInferredError):
            Loadumper._invoke(
                open_mode=OpenMode.READ,
            )

    def test_loadump(self):
        # generalized function, tests are described in dump or load module.
        pass
