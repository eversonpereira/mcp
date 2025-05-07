import importlib.util
import os
import sys
import inspect
from typing import Any

PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), "../plugins")
PLUGIN_FOLDER = os.path.abspath(PLUGIN_FOLDER)

def load_plugins():
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and not filename.startswith("__"):
            filepath = os.path.join(PLUGIN_FOLDER, filename)
            module_name = f"plugins.{filename[:-3]}"
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

def execute_plugin(name: str, args: dict[str, Any]) -> Any:
    try:
        module = importlib.import_module(f"app.plugins.{name}")
        if hasattr(module, "run"):
            sig = inspect.signature(module.run)
            if len(sig.parameters) == 1 and "prompt" in sig.parameters:
                return module.run(args.get("prompt", ""))
            return module.run(**args)
        else:
            return f"Plugin '{name}' não possui função 'run'."
    except Exception as e:
        return f"Erro ao executar plugin '{name}': {str(e)}"

def list_available_plugins():
    plugins = []
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                name = filename[:-3]
                module = importlib.import_module(f"app.plugins.{name}")
                desc = module.describe() if hasattr(module, "describe") else "Sem descrição."
                plugins.append(f"- {name}: {desc}")
            except:
                continue
    return "\n".join(plugins)

