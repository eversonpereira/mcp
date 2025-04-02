# 🧠 MCP - Model Context Protocol

Projeto completo para uma aplicação conversacional com:

- ✅ FastAPI + JWT
- ✅ LLM local via Ollama (ex: Mistral)
- ✅ Contexto com memória vetorial (ChromaDB)
- ✅ Suporte a múltiplos usuários e sessões
- ✅ Resumo automático de histórico longo
- ✅ Sistema de plugins para executar ações reais

---

## 🚀 Como rodar

### 1. Clone o projeto e crie o ambiente

```bash
git clone <repo>
cd mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure o .env
```env
MODEL_NAME=mistral
VECTOR_DB_PATH=./chroma
DB_PATH=./mcp.db
CONTEXT_LIMIT=5
SUMMARY_TRIGGER=20
```

### 3. Inicie o Ollama
```bash
ollama run mistral
```

### 4. Suba o servidor
```bash
chmod +x start.sh
./start.sh
```

## 🛡️ Autenticação
- POST /auth/register: Cria novo usuário

- POST /auth/login: Retorna token JWT

Use o token JWT nas requisições para /mcp/chat.

## 🤖 Plugins
Para chamar um plugin:
```json
{
  "session_id": "sessao01",
  "prompt": "plugin: {\"name\": \"list_files\", \"args\": {\"path\": \"/etc\"}}"
}
```

## 📁 Estrutura
```bash
app/
├── routes/         # Rotas da API
├── services/       # Lógica de negócio (MCP, plugins, memória)
├── db/             # Persistência (SQLite e vetorial)
├── models/         # Schemas Pydantic
├── plugins/        # Plugins executáveis pelo MCP
├── auth/           # Login, JWT, usuários
```

## 📬 Contato
Desenvolvido por [Everson 🧠].
