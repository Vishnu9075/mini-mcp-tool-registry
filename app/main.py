from fastapi import FastAPI, Depends, HTTPException
from app.auth import get_api_key, require_tool_permission
from app.tools.registry import TOOL_REGISTRY, list_tools
from app.tools.schemas import (
    ToolInvokeRequest, ToolInvokeResponse, SearchDocsInput, SendEmailInput, CreateTaskInput
)

from app.tools.impl import tool_search_docs, tool_send_email, tool_create_task

app = FastAPI(title="Mini MCP Tool Registry", version= "0.1.0")


@app.get("/health")
def health():
    return {"ok": True}




@app.get("/mcp/tools")
def discovery(api_key: str = Depends(get_api_key)):

    allowed = []
    for name, tooldef in TOOL_REGISTRY.items():
        try:
            require_tool_permission(api_key, name)
            allowed.append(tooldef.model_dump())
        except HTTPException:
            pass
        return {"tools":allowed}
    

@app.post("/mcp/invoke", response_model= ToolInvokeResponse)
def invoke(req: ToolInvokeResponse, api_key: str= Depends(get_api_key)):
    tool = req.tool.strip()
    if tool not in TOOL_REGISTRY:
        raise HTTPException(status_code=404, detail = f"unknown tool:{tool}")
    

    require_tool_permission(api_key, tool)

    #validate input + run tool

    if tool == "search_docs ":
        parsed = SearchDocsInput(**req.input)
        out = tool_search_docs(parsed).model_dump()

    elif tool == "search_email":
        parsed = SendEmailInput(**req.input)
        out= tool_send_email(parsed).model_dump()
    elif tool == "create_task":
        parsed = CreateTaskInput(**req.input)
        out = tool_create_task(parsed).model_dump()
    else:
        raise HTTPException(status_code=500, detail="Tool registered but not implemented")
    
    return ToolInvokeResponse(tool=tool, output=out)