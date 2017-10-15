from enum import Enum

import subprocess, os, re, codecs
import logging, importlib

logger = logging.getLogger(__name__)
SAMPLE_OBJ = [1,2,3]

class DumpMode(Enum):
    WRITE = "w"
    APPEND = "a"
    EXCLUSIVE_CREATION = "x"
    READ = "r"

class ExtensionNotInferredError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "extension of file cannot be infered. put proper filename or format."

class CharsetNotInferredError(Exception):
    def __init__(self, stdout):
        self.msg = "".join(stdout.split(":")[1:])[1:]
        pass
    def __str__(self):
        return "charset of file cannot be inferred. ERROR msg : {}".format(self.msg)

class Loadumper():
    tb_mapping = {"json": False, "pickle": True, "yaml": False, "toml": False}

    def __init__(self, tbs):
        self.tb_mapping.update(tbs)
    """
    detect file is binary or not(text).
    may raise CharsetNotInferredError
    """
    def _is_binary(self, filename):
        ext = self._extract_extension(filename)
        res = self.tb_mapping.get(ext)
        if res is not None: return res
        if os.path.exists(filename):
            commands = ["file", "--mime", filename]
            stdout = subprocess.run(commands, stdout=subprocess.PIPE, check=True).stdout.decode('utf-8')
            m = re.search("charset=(.*)", stdout)
            if m is None: raise CharsetNotInferredError(stdout)
            return True if m.group(1) == "binary" else False
        else: # if mode is write or append or exclusive creation.
            if ext == "": return False # assume text-mode.
            try:
                return isinstance(importlib.import_module(ext).dumps(SAMPLE_OBJ), bytes)
            except AttributeError:
                raise CharsetNotInferredError(
                    "{} module has no dumps method to analyze bynary or text".format()
                )

    @staticmethod
    def _extract_extension(file):
        return os.path.splitext(file)[1][1:]


    """
    may raise ExtensionInferenceError
    """
    @staticmethod
    def _invoke(dump_mode: DumpMode, filename=None, fmt=None):
        ext = Loadumper._extract_extension(filename) if filename else fmt
        if ext is None: raise ExtensionNotInferredError
        target = importlib.import_module(ext)
        # "[load|dump]s?"
        method_mappings = dict(zip(list("rawx"), ["load"] + ["dump"] * 3))
        method = getattr(target, method_mappings[dump_mode.value] + 's' * (not filename))
        logger.debug("module : {}, method : {}".format(target, method))
        return method

    """
    generalized [load|dump]s? function
    """
    def loadump(self, dump_mode: DumpMode, *,
                obj=None, s=None, filename=None, fmt=None, encoding=None, errors=None, buffering=None, **kwargs):
        # load method precedes loads
        if obj is not None:
            if s is not None:
                logger.warning("`obj` & `s` are both not-None, so `s` is forced to set None")
                s=None

        if filename is None:
            return self._invoke(dump_mode=dump_mode, fmt=fmt)(obj or s, **kwargs)
        else:
            mode = dump_mode.value + "b"*self._is_binary(filename)
            codecs_kwargs = \
                {k:v for k,v in dict(mode=mode, encoding=encoding, errors=errors, buffering=buffering).items() \
                    if v is not None}
            with codecs.open(filename=filename, **codecs_kwargs) as fp:
                return self._invoke(dump_mode=dump_mode, filename=filename, fmt=fmt)(fp, **kwargs)
