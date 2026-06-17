from fastapi import APIRouter, Request, Header
from typing import Optional
from datetime import datetime

router = APIRouter()

# In-memory store for events (optional, for debugging)
latest_github_event = {}

@router.post("/github")
async def github_webhook(request: Request, x_github_event: Optional[str] = Header(None)):
    payload = await request.json()
    
    # Fast parsing and acknowledgment to meet < 500ms latency requirement.
    # Note: Using FastAPI, this endpoint inherently has very low latency.
    global latest_github_event
    latest_github_event = {
        "event": x_github_event,
        "repo": payload.get("repository", {}).get("full_name"),
        "pusher": payload.get("pusher", {}).get("name"),
        "commits": len(payload.get("commits", [])),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # print('Stored GitHub event:', latest_github_event)
    return {"received": True}
