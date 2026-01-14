from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any



class SearchDocsInput(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)

class SearchDocsResult(BaseModel):
    id : str
    title : str
    snippet : str

class SearchDocsOutput(BaseModel):
    results : List[SearchDocsResult]

class SendEmailInput(BaseModel):
    to : EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    body : str = Field(..., min_length=1, max_length=10000)

class SendEmailOutput(BaseModel):
    status : str
    task_id : str

class CreateTaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    due_iso: Optional[str] = Field(default=None, description="ISO datetime string (optional)")
    notes: Optional[str] = Field(default=None, max_length=2000)

class CreateTaskOutput(BaseModel):
    status: str
    task_id: str


# Generic invoke wrapper (like a tiny MCP-ish call format)

class ToolInvokeRequest(BaseModel):
    tool : str
    input : Dict[str, Any]

class ToolInvokeResponse(BaseModel):
    tool : str
    output : Dict[str, Any]