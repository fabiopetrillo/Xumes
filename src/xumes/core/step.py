
class Step:

    def __init__(self, func, content, params=None):
        if params is None:
            params = {}
        self.func = func
        self.content = content
        self.params = params
