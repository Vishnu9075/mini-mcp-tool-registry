from typing import List
import uuid

from app.storage import DOCS, create_task_record

from .schemas import(
    SearchDocsInput, SearchDocsOutput, SearchDocsResult, SendEmailInput, SendEmailOutput,
    CreateTaskInput, CreateTaskOutput
)


def tool_search_docs(payload: SearchDocsInput) -> SearchDocsOutput:
    q = payload.query.lower().strip()
    scored = []
    for d in DOCS:
        text = (d.title + " " + d.body).lower()
        score = text.count(q) if q else 0
        if q in text:
            scored.append((score, d))

    scored.sort(key=lambda x: x[0], reverse=True)