import inspect
import os
from typing import List, Dict

from xumes.core.step import Step


def create_registry_content():
    registry: Dict[str, List[Step]] = {}

    def registrar(content: str):
        def decorator(func):
            file_path = inspect.getsourcefile(func)
            file_name = os.path.basename(file_path[:-3])
            if file_name not in registry:
                registry[file_name] = [Step(func, content)]
            else:
                registry[file_name].append(Step(func, content))
            return func

        registrar.all = registry
        return decorator

    return registrar


def exec_registry_function(registry: List[Step], game_context):
    """
    Execute all functions from registry
    :param registry:  of functions
    :param game_context: where the functions will be executed
    """
    for r in registry:
        r.func(game_context, **r.params)


def get_content_from_registry(registry: List[Step]):
    """
    Get all content from registry
    :param registry:  we want to get the content
    """
    return [step.content for step in registry]


def create_registry():
    registry = {}

    def registrar(func):
        file_path = inspect.getsourcefile(func)
        file_name = os.path.basename(file_path[:-3])
        registry[file_name] = func
        return func

    registrar.all = registry
    return registrar
