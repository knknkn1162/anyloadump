from .loadump import loadump, DumpMode

def dump(obj, file, *, encoding=None, errors=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.WRITE, file=file, encoding=encoding, errors=errors, **kwargs)

def adump(obj, file, *, encoding=None, errors=None, **kwargs):
    return loadump(
        obj=obj,
        dump_mode=DumpMode.APPEND,
        file=file,
        encoding=encoding,
        errors=errors,
        **kwargs
    )

def xdump(obj, file, *, encoding=None, errors=None, **kwargs):
    return loadump(
        obj=obj,
        dump_mode=DumpMode.EXCLUSIVE_CREATION,
        file=file,
        encoding=encoding,
        errors=errors,
        **kwargs
    )

def dumps(obj, *, encoding=None, errors=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.WRITE, encoding=encoding, errors=errors, **kwargs)

def adumps(obj, *, encoding=None, errors=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.APPEND, encoding=encoding, errors=errors, **kwargs)

def xdumps(obj, *, encoding=None, errors=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.EXCLUSIVE_CREATION, encoding=encoding, errors=errors, **kwargs)
