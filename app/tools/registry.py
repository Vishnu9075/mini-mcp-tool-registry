from typing import Dict, Any
from pydantic import BaseModel
from .schemas import SearchDocsInput, SendEmailInput, CreateTaskInput


class ToolDef(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

def pydantic_schema(model) -> Dict[str, Any]:
    #pydantic v2 json schema
    return model.model_json_schema()


TOOL_REGISTRY: Dict[str, ToolDef] = {
    "search_docs": ToolDef(
        name="search_docs",
        description="Search internal docs using a simple substring matcher .",
        input_schema= pydantic_schema(SearchDocsInput)
    ),

    "send_email": ToolDef(
        name="create_task",
        description="Creates a task record ( demo implementation).",
        input_schema= pydantic_schema(CreateTaskInput),
    ),

    "create_task": ToolDef(
        name="create_task",
        description="Creates a task record ( demo in-memory storage )",
        input_schema=pydantic_schema(CreateTaskInput),
    ),
}


def list_tools() -> Dict[str, Any]:
    return {
        "tool": [t.model_dump() for t in TOOL_REGISTRY.values()]
    }