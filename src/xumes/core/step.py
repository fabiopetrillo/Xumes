
class Step:

    def __init__(self, func, content):
        self.func = func
        self.content = content
        self.params = {}

    def add_params(self, scenario_name, params):
        self.params[scenario_name] = params
