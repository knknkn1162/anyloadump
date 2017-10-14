from .loadump import loadump, DumpMode

def load(file, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(DumpMode.READ, file=file, encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def loads(s, *, encoding=None, errors=None, buffering=None, **kwargs):
    return load(DumpMode.READ, s=s, encoding=encoding, errors=errors, buffering=buffering, **kwargs)
