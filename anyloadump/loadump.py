from enum import Enum

import subprocess
import os
import re
import codecs

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


class ExtensionNotFoundError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "cannot extract file_extension from {}".format(self.filename)

class CharsetNotInferredError(Exception):
    def __init__(self, stdout):
        self.msg = "".join(stdout.split(":")[1:])[1:]
        pass
    def __str__(self):
        return "charset of file cannot be inferred. ERROR msg : {}".format(self.msg)


"""
detect file is binary or not(text).
may raise CalledProcessError or FileNotFoundError
"""
def _is_binary(file):
    stdout = subprocess.run(["file", "--mime", file], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8')
    m = re.search("charset=(.*)", stdout)
    if m is None: raise CharsetNotInferredError(stdout)
    return True if m.group(1) == "binary" else False



"""
may raise ExtensionNotFoundError
"""
def _extract_extension(file):
    try:
        return os.path.splitext(file)[1][1:]
    except KeyError:
        raise ExtensionNotFoundError


"""
may raise ExtensionInferenceError
"""
def _invoke(dump_mode: DumpMode, file=None, fmt=None):
    ext = _extract_extension(file) if file else fmt
    if ext is None: raise ExtensionNotInferredError
    target = _extract_extension(file).__import__(ext)
    # "[load|dump]s?"
    method_mappings = dict(zip(list("rawx"), ["load"] + ["dump"] * 3))
    return getattr(target, method_mappings[dump_mode.value] + 's' * (not file))

"""
generalized [load|dump]s? function
"""
def loadump(dump_mode: DumpMode, *, obj=None, file=None, fmt = None, encoding=None, errors=None, **kwargs):

    kwargs.update(
        dict(
            encoding=encoding,
            errors=errors,
            obj=obj,
        )
    )
    kwargs = {k: v for k, v in kwargs if k is not None}

    if file is None:
        return _invoke(dump_mode=dump_mode, fmt=fmt)(**kwargs)
    else:
        if not os.path.exists(file): raise FileNotFoundError
        mode = dump_mode.value + ("b" if _is_binary(file) else "")
        with codecs.open(file, mode=mode, encoding=encoding, errors=errors) as fp:
            return _invoke(dump_mode=dump_mode, file=file, fmt=fmt)(fp=fp, **kwargs)
