import importlib
import os
import sys

class AutoLoader:

    modules: dict = dict()
    base_path: str = os.path.dirname(sys.modules['__main__'].__file__)

    @classmethod
    def load(cls):
        for root, directory, files in os.walk(cls.base_path):
            directory[:] = [d for d in directory if d != ".venv"]
            for file in files:
                if not file.endswith(".py") or file == "__init__.py": continue
                module_path = os.path.relpath(os.path.join(root, file), cls.base_path)
                module_name = module_path.replace(os.sep, ".").rsplit(".py", 1)[0]
                cls.modules[module_name] = importlib.import_module(module_name)
