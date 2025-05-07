from app.models.context import UserPrompt, MCPResponse
from app.services.llm_wrapper import ask_llm
from app.services.memory import get_context_memory, store_interaction, maybe_summarize_session
from app.services.actions import execute_plugin, list_available_plugins
import json
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

KEYWORDS_FOR_CNPJ = ["cnpj", "empresa", "sócio", "socios", "razao social", "estabelecimento", "capital", "qualificação"]

CNPJ_SCHEMA = """
Tabelas disponíveis:

Empresas (CNPJ, RAZAOSOCIAL, NATUREZAJURIDICA, `QUAL-RESPONS`, `CAP-SOCIAL`, `PORTE-EMP`, `ENTE-FEDERATIVO`)
Estabelecimentos (CNPJ, IDENTIFICADOR, RAZAO, `MATRIZ-FILIAL`, RAZAOSOCIAL, SITUACAO, `DATA-CADASTRO`, MOTIVO, CIDADE, `NM-PAIS`, `DATA-INICIO`, `CNAE-FISCAL`, `CNAE-FISCAL2`, `TIPO-LOGRADOURO`, LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO, CEP, UF, `CODIGO-MUNICIPIO`, EMAIL)
Socios (CNPJ, IDENT, NOME, CPF, QUALIFICACAO, `DATA-ENTRADA`, PAIS, `NOME-REPRES`)
Cnaes (COD, Descricao)
"""

def process_prompt(input_data: UserPrompt) -> MCPResponse:
    context = get_context_memory(input_data.user_id, input_data.session_id, input_data.prompt)
    full_prompt = "\n".join(context + [input_data.prompt])

    detection_instruction = (
        "Você é um orquestrador. Dado um prompt de usuário, se ele puder ser resolvido com um dos plugins abaixo, "
        "responda APENAS com um JSON no formato {\"name\": \"plugin_name\", \"args\": {chave: valor}}.\n"
        "Use a chave 'prompt' quando quiser passar a instrução completa para o plugin.\n"
        + list_available_plugins() + "\n\nPrompt do usuário:\n" + input_data.prompt
    )

    detection = ask_llm(detection_instruction)
    logger.info(f"LLM Detection Output: {detection}")

    try:
        parsed = json.loads(detection)
        if "name" in parsed:
            plugin_name = parsed["name"]
            plugin_args = parsed.get("args", {})
            logger.info(f"Plugin detectado: {plugin_name} com args: {plugin_args}")

            # Corrige uso incorreto de 'query' ou 'sql' para 'prompt' e injeta schema
            if plugin_name == "mysql_cnpj":
                plugin_args = {"prompt": input_data.prompt + "\n\n" + CNPJ_SCHEMA}

            result = execute_plugin(plugin_name, plugin_args)

            store_interaction(input_data.user_id, input_data.session_id, input_data.prompt, result)
            return MCPResponse(response=result, context_used=context)

    except Exception as e:
        logger.warning(f"Falha ao interpretar JSON da LLM: {detection}\nErro: {str(e)}")

    response = ask_llm(full_prompt)
    store_interaction(input_data.user_id, input_data.session_id, input_data.prompt, response)
    maybe_summarize_session(input_data.user_id, input_data.session_id)

    return MCPResponse(response=response, context_used=context)

