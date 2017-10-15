from .loadump import Loadumper, DumpMode

def dump(obj, filename, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, dump_mode=DumpMode.WRITE, filename=filename,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adump(obj, file, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(
        obj=obj,
        dump_mode=DumpMode.APPEND,
        filename=file,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def xdump(obj, filename, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(
        obj=obj,
        dump_mode=DumpMode.EXCLUSIVE_CREATION,
        filename=filename,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def dumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, dump_mode=DumpMode.WRITE,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, dump_mode=DumpMode.APPEND,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def xdumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, dump_mode=DumpMode.EXCLUSIVE_CREATION,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)
