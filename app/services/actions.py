import os
import importlib.util
from typing import Callable

PLUGINS = {}

PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), "..", "plugins")


def load_plugins():
    if not os.path.exists(PLUGIN_FOLDER):
        os.makedirs(PLUGIN_FOLDER)

    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            file_path = os.path.join(PLUGIN_FOLDER, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "run") and callable(module.run):
                PLUGINS[module_name] = module.run


def execute_plugin(name: str, args: dict) -> str:
    if name not in PLUGINS:
        return f"Plugin '{name}' não encontrado."
    try:
        return PLUGINS[name](**args)
    except Exception as e:
        return f"Erro ao executar plugin '{name}': {str(e)}"
