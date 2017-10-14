from enum import Enum

import subprocess, os, re, codecs
import logging, importlib

logger = logging.getLogger(__name__)

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


"""
detect file is binary or not(text).
may raise CharsetNotInferredError or FileNotFoundError
"""
def _is_binary(file):
    if not os.path.exists(file): raise FileNotFoundError(file)
    commands = ["file", "--mime", file]
    stdout = subprocess.run(commands, stdout=subprocess.PIPE, check=True).stdout.decode('utf-8')
    m = re.search("charset=(.*)", stdout)
    if m is None: raise CharsetNotInferredError(stdout)
    return True if m.group(1) == "binary" else False


def _extract_extension(file):
    return os.path.splitext(file)[1][1:]


"""
may raise ExtensionInferenceError
"""
def _invoke(dump_mode: DumpMode, filename=None, fmt=None):
    ext = _extract_extension(filename) if filename else fmt
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
def loadump(dump_mode: DumpMode, *,
            obj=None, s=None, filename=None, fmt=None, encoding=None, errors=None, buffering=None, **kwargs):
    # load method precedes loads
    if obj is not None:
        logger.warning("`obj` & `s` are both None, so `s` is forced to set None")
        s=None

    kwargs.update(
        dict(
            obj=obj,
            s=s,
        )
    )
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if filename is None:
        return _invoke(dump_mode=dump_mode, fmt=fmt)(**kwargs)
    else:
        if not os.path.exists(file): raise FileNotFoundError
        mode = dump_mode.value + ("b" if _is_binary(file) else "")
        with codecs.open(file, mode=mode, encoding=encoding, errors=errors) as fp:
            return _invoke(dump_mode=dump_mode, file=file, fmt=fmt)(fp=fp, **kwargs)
