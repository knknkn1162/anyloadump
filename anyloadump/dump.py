from .loadump import loadump, DumpMode

def dump(obj, filename, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.WRITE, filename=filename,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adump(obj, file, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(
        obj=obj,
        dump_mode=DumpMode.APPEND,
        filename=file,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def xdump(obj, filename, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(
        obj=obj,
        dump_mode=DumpMode.EXCLUSIVE_CREATION,
        filename=filename,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def dumps(obj, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.WRITE,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adumps(obj, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.APPEND,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def xdumps(obj, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(obj=obj, dump_mode=DumpMode.EXCLUSIVE_CREATION,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)
