import datetime
import importlib


class BaseBackend(object):
    def __init__(self, year=2012):
        self.start_date = datetime.datetime(year, 1, 1)
        self.end_date = datetime.datetime(year + 1, 12, 31)


def get_backend(name):
    module_path = 'readables.backends.%s' % name
    module = importlib.import_module(module_path)
    return getattr(module, 'Backend')
