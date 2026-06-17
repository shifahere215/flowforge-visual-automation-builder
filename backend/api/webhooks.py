from fastapi import APIRouter, Request, Header
from typing import Optional
from datetime import datetime

router = APIRouter()

# In-memory store for events (optional, for debugging)
latest_github_event = {}

import asyncio
from api.workflows import DEPLOYED_WORKFLOWS
from engine.dag import execute_workflow

@router.post("/github")
async def github_webhook(request: Request, x_github_event: Optional[str] = Header(None)):
    payload = await request.json()
    
    # Fast parsing and acknowledgment to meet < 500ms latency requirement.
    global latest_github_event
    latest_github_event = {
        "event": x_github_event,
        "repo": payload.get("repository", {}).get("full_name"),
        "pusher": payload.get("pusher", {}).get("name"),
        "commits": len(payload.get("commits", [])),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Iterate through deployed workflows and find any with a github trigger
    # In a real app, this would query a database for active subscriptions.
    for wf_id, deployment in DEPLOYED_WORKFLOWS.items():
        workflow = deployment["workflow"]
        execution_order = deployment["execution_order"]
        
        has_github_trigger = any(
            node.role == "trigger" and ("github" in node.data.label.lower() or "webhook" in node.data.label.lower())
            for node in workflow.nodes
        )
        
        if has_github_trigger:
            print(f"⚡ Triggering deployed workflow {wf_id}...")
            # Execute the workflow in the background to not block the webhook response
            asyncio.create_task(
                execute_workflow(workflow, execution_order, initial_context={"github_event": latest_github_event})
            )
            
    return {"received": True}
