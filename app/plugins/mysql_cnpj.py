import os
import pymysql
from app.services.llm_wrapper import ask_llm
from dotenv import load_dotenv

load_dotenv()

SCHEMA_CNPJ = """
Tabelas disponíveis:

Empresas (CNPJ, RAZAOSOCIAL, NATUREZAJURIDICA, `QUAL-RESPONS`, `CAP-SOCIAL`, `PORTE-EMP`, `ENTE-FEDERATIVO`)
Estabelecimentos (CNPJ, IDENTIFICADOR, RAZAO, `MATRIZ-FILIAL`, RAZAOSOCIAL, SITUACAO, `DATA-CADASTRO`, MOTIVO, CIDADE, `NM-PAIS`, `DATA-INICIO`, `CNAE-FISCAL`, `CNAE-FISCAL2`, `TIPO-LOGRADOURO`, LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO, CEP, UF, `CODIGO-MUNICIPIO`, EMAIL)
Socios (CNPJ, IDENT, NOME, CPF, QUALIFICACAO, `DATA-ENTRADA`, PAIS, `NOME-REPRES`)
Cnaes (COD, Descricao)
"""

def gerar_sql(prompt: str) -> str:
    full_prompt = (
        "Você é um assistente especializado em bancos MySQL."
        "Considere apenas as tabelas e campos abaixo, os campos estão entre parênteses após o nome das tabelas."
        "Gere uma consulta para o pedido abaixo baseado nessa estrutura:"
        + SCHEMA_CNPJ +
        f"\nPedido: {prompt}\n"
        "Retorne apenas a query SQL, sem nenhuma explicação."
    )
    return ask_llm(full_prompt)

def executar_query(query: str) -> str:
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                if not result:
                    return "Nenhum dado encontrado."
                return str(result)
    except Exception as e:
        return f"Erro ao executar consulta: {str(e)}"

def run(prompt: str) -> str:
    query = gerar_sql(prompt)
    if not query.strip().lower().startswith("select"):
        return f"Não foi possível gerar uma query válida: {query}"
    return executar_query(query)

def describe():
    return "Interpreta perguntas sobre empresas, CNPJs ou sócios e executa consultas no banco MySQL."

def parameters():
    return {"prompt": "Texto da pergunta sobre empresa ou sócio"}

