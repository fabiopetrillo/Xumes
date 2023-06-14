import functools


class C:

    def __init__(self):
        self.value = 0

    def set_value(self, v):
        self.value = v

    def __str__(self):
        return str(self.value)


def notify_decorator(func):
    @functools.wraps(func)
    def wrapper(self, *arg, **kw):
        if func.__name__ != "notify":
            res = func(self, *arg, **kw)
            self.notify()
            return res

    return wrapper


class Test:

    def __init__(self, obj):
        self.obj = obj
        self.attributes = ["value"]

    def notify(self):
        print("notify")

    @notify_decorator
    def __getattr__(self, *args):
        return self.obj.__getattribute__(*args)

    @notify_decorator
    def __setattr__(self, *args):
        return self.obj.__setattr__(*args)

    @notify_decorator
    def __add__(self, other):
        return self.obj + other

    def state(self):
        return {attr: self.obj.__getattribute__(attr) for attr in self.attributes}


t = Test(C())
t.set_value(2)

t2 = Test(5)
t2 = t2 + 1





