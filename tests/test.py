
class C:

    def __init__(self):
        self.value = 0

    def set_value(self, v):
        self.value = v

    def __str__(self):
        return str(self.value)


class Test:

    def __init__(self, obj):
        self.obj = obj

    def notify(self):
        print("notify")

    def __getattr__(self, *args):
        self.notify()
        return self.obj.__getattribute__(*args)

    def __str__(self):
        return self.obj.__str__()


t = Test(C())
t.set_value(2)

