import asyncio
import os
import aiohttp
from typing import Dict, Any
from schemas import Node
from dotenv import load_dotenv

load_dotenv()

async def trigger_node_handler(node: Node, context: Dict[str, Any]) -> Any:
    # If a real webhook triggered this, it's in the initial context
    github_event = context.get("github_event", {"event": "manual_test", "pusher": "unknown"})
    print(f"Trigger {node.id} captured event: {github_event}")
    return github_event

async def action_node_handler(node: Node, context: Dict[str, Any]) -> Any:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print(f"⚠️ Action {node.id}: DISCORD_WEBHOOK_URL not configured. Simulating success.")
        return {"status": "simulated", "node_id": node.id}

    # Find the trigger data in context. 
    # Usually we'd resolve expressions like {{trigger.pusher}}, but for demo we just grab the first trigger's output.
    trigger_data = context.get("github_event", {})
    pusher = trigger_data.get("pusher", "Someone")
    commits = trigger_data.get("commits", 0)
    repo = trigger_data.get("repo", "a repository")

    content = f"🚀 **{pusher}** just pushed **{commits}** commits to `{repo}`! (from kagakoko)"

    payload = {
        "content": content,
        "username": "kagakoko",
        # Optional avatar:
        # "avatar_url": "https://i.imgur.com/4M34hi2.png"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status in (200, 204):
                    print(f"✅ Discord message sent for node {node.id}")
                    return {"status": "success", "node_id": node.id}
                else:
                    err_text = await response.text()
                    print(f"❌ Discord webhook failed: {response.status} {err_text}")
                    return {"status": "error", "error": err_text}
    except Exception as e:
        print(f"❌ Discord action error: {e}")
        return {"status": "error", "error": str(e)}

NODE_REGISTRY = {
    "trigger": trigger_node_handler,
    "action": action_node_handler,
}
