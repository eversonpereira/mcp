from pydantic import BaseModel

class UserPrompt(BaseModel):
    user_id: str
    session_id: str
    prompt: str

class MCPResponse(BaseModel):
    response: str
    context_used: list[str]
