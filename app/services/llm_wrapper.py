import subprocess

def ask_llm(prompt: str) -> str:
    try:
        result = subprocess.run(["ollama", "run", "mistral"], input=prompt.encode(), capture_output=True, timeout=60)
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"[ERRO NA LLM]: {str(e)}"

