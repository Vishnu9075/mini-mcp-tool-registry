from fastapi import Header,HTTPException
from typing import Optional, set, Dict

# Simple API-key permissions model (replace with DB later)

API_KEYS : Dict[str, set[str]] = {
    # full access key
    "dev_full_access_key": {"search_doc", "send_email", "create_task"},
    #read-only key
    "dev_doc_only_key" : {"search_docs"},
    #task-only key
    "dev_task_only_key" : {"create_task"},
}

def get_api_key(authorization : Optional[str] = Header(default=None))-> str:
    if not authorization or not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="missing/invalid authorization header")
    
    key = authorization.replace("Bearer ", "").strip()

    if key not in API_KEYS:
        raise HTTPException(status_code=403, detail="invalid API key")
    return key


def require_tool_permission(api_key : str, tool_name:str) -> None:
    allowed = API_KEYS.get(api_key, set())
    if tool_name not in allowed:
        raise HTTPException(status_code=403, 
                            detail=f"API key not permitted to use tool: {tool_name}",)