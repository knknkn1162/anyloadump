from .loadump import loadump, DumpMode

def load(file, *, encoding=None, errors=None, **kwargs):
    return loadump(DumpMode.READ, file=file, encoding=encoding, errors=errors, **kwargs)
