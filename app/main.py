from fastapi import FastAPI
from app.routes import mcp
from app.routes import auth
from app.db.vector_store import initialize_vector_store
from app.db.history_store import initialize_history_store
from app.services.actions import load_plugins

app = FastAPI(title="MCP - Model Context Protocol")

initialize_vector_store()
initialize_history_store()
load_plugins()

app.include_router(auth.router)
app.include_router(mcp.router)

@app.get("/")
def root():
    return {"message": "MCP API está no ar!"}

