#!/bin/bash

# Ativa o ambiente virtual
source .venv/bin/activate

# Seta o caminho base para os imports funcionarem corretamente
export PYTHONPATH=.

# Inicia o servidor FastAPI via uvicorn na porta 8001
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

