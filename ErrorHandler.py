import functools


class CatchException:
    def __init__(self, f):
        self.f = f
        functools.update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        try:
            return self.f(*args, **kwargs)
        except Exception as e:
            print('Caught an exception in', self.f.__name__)


class ErrorCatcher(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = CatchException(dct[m])
        return type.__new__(cls, name, bases, dct)