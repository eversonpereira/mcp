from app.models.context import UserPrompt, MCPResponse
from app.services.llm_wrapper import ask_llm
from app.services.memory import get_context_memory, store_interaction, maybe_summarize_session
from app.services.actions import execute_plugin
import json

def process_prompt(input_data: UserPrompt) -> MCPResponse:
    context = get_context_memory(input_data.user_id, input_data.session_id, input_data.prompt)
    full_prompt = "\n".join(context + [input_data.prompt])

    if input_data.prompt.startswith("plugin:"):
        try:
            _, plugin_raw = input_data.prompt.split("plugin:", 1)
            plugin_data = json.loads(plugin_raw.strip())
            plugin_name = plugin_data["name"]
            plugin_args = plugin_data.get("args", {})
            result = execute_plugin(plugin_name, plugin_args)
            store_interaction(input_data.user_id, input_data.session_id, input_data.prompt, result)
            return MCPResponse(response=result, context_used=context)
        except Exception as e:
            return MCPResponse(response=f"Erro ao interpretar plugin: {str(e)}", context_used=context)

    response = ask_llm(full_prompt)

    store_interaction(input_data.user_id, input_data.session_id, input_data.prompt, response)
    maybe_summarize_session(input_data.user_id, input_data.session_id)

    return MCPResponse(response=response, context_used=context)
