from fastapi import APIRouter, Depends
from app.models.context import UserPrompt, MCPResponse
from app.services.mcp_core import process_prompt
from app.auth.auth_handler import get_current_user

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.post("/chat", response_model=MCPResponse)
def mcp_chat(input_data: UserPrompt, user=Depends(get_current_user)):
    input_data.user_id = user["id"]
    return process_prompt(input_data)
