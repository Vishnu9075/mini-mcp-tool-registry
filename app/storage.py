from typing import List, Dict
from dataclasses import dataclass
import uuid
from datetime import datetime


@dataclass
class Doc:
    id: str
    title: str
    body: str


DOCS: List[Doc] = [
    Doc(id= "d1", title= "MCP Overview", body="Model Context Protocol enables tools and context exchange."),
    Doc(id="d2", title=" PKCE Notes", body="PKCE uses a code_verifier and code_challenge for OAuth security."),
    Doc(id="d3",title="FastAPI Tips", body="Use dependency injection for auth, and pydantic for schemas."),
    Doc(id="d4", title="Tool Registry", body="Expose tools with JSON Schema and enforce permissions per tool."),
]


TASKS: Dict[str, dict]={}

def create_task_record(title: str, due_iso: str | None, notes: str |None) -> str:
    task_id = "t_" + uuid.uuid4().hex[:12]

    TASKS[task_id] = {
        "id": task_id,
        "title": title,
        "due_iso": due_iso,
        "notes": notes,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    return task_id