import os

def run(path: str = ".") -> str:
    if not os.path.exists(path):
        return f"Caminho '{path}' não existe."

    items = os.listdir(path)
    return "\n".join(items)
