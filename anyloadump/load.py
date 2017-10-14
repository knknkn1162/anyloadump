from .loadump import loadump, DumpMode

def load(filename, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(DumpMode.READ, filename=filename, encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def loads(s, *, encoding=None, errors=None, buffering=None, **kwargs):
    return loadump(DumpMode.READ, s=s, encoding=encoding, errors=errors, buffering=buffering, **kwargs)
