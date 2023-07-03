import inspect
import os


def create_registry_content():
    registry = {}

    def registrar(content: str):
        def decorator(func):
            file_path = inspect.getsourcefile(func)
            file_name = os.path.basename(file_path[:-3])
            registry[file_name] = (func, content)
            return func

        registrar.all = registry
        return decorator

    return registrar


def create_registry():
    registry = {}

    def registrar(func):
        file_path = inspect.getsourcefile(func)
        file_name = os.path.basename(file_path[:-3])
        registry[file_name] = func
        return func

    registrar.all = registry
    return registrar
