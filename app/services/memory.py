from app.db.history_store import store_history, get_history, count_history
from app.db.vector_store import add_to_vector_store, query_similar_context
from app.config import settings
from app.services.llm_wrapper import ask_llm

def get_context_memory(user_id: str, session_id: str, latest_prompt: str) -> list[str]:
    history = get_history(user_id, session_id)
    flat_history = [h["prompt"] + "\n" + h["response"] for h in history[-settings.CONTEXT_LIMIT:]]
    semantic_hits = query_similar_context(user_id, session_id, latest_prompt)
    return semantic_hits + flat_history

def store_interaction(user_id: str, session_id: str, prompt: str, response: str):
    store_history(user_id, session_id, prompt, response)
    add_to_vector_store(user_id, session_id, prompt + "\n" + response)

def maybe_summarize_session(user_id: str, session_id: str):
    total = count_history(user_id, session_id)
    if total >= settings.SUMMARY_TRIGGER:
        full_history = get_history(user_id, session_id)
        joined = "\n".join(h["prompt"] + "\n" + h["response"] for h in full_history)
        summary = ask_llm("Resuma a seguinte sessão:\n" + joined)
        store_history(user_id, session_id, "[RESUMO]", summary)
