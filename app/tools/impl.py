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
    top = [d for _, d in scored[: payload.top_k]]


    results: List[SearchDocsResult] = []
    for d in top:
        idx = d.body.lower().find(q)
        start = max(idx - 40, 0) if idx >= 0 else 0
        end = min(start + 140, len(d.body))
        snippet = d.body[start:end]
        results.append(SearchDocsResult(id=d.id, title=d.title, snippet=snippet))

    return SearchDocsOutput(results=results)



def tool_send_email(payload: SendEmailInput) -> SendEmailOutput:
    # Demo-only: in real life you’d integrate SMTP / SendGrid / Gmail API etc.
    # We’ll just return a fake message_id.

    msg_id = "m_" + uuid.uuid4().hex[:12]
    return SendEmailOutput(status="sent", message_id=msg_id)



def tool_create_task(payload: CreateTaskInput) -> CreateTaskOutput:
    task_id = create_task_record(payload.title, payload.due_iso, payload.notes)
    return CreateTaskOutput(status="created", task_id=task_id)