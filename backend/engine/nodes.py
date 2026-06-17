import asyncio
from typing import Dict, Any
from schemas import Node

async def trigger_node_handler(node: Node, context: Dict[str, Any]) -> Any:
    # Simulate trigger extracting data
    await asyncio.sleep(0.01)
    print(f"Trigger {node.id} executed")
    return {"event": "trigger_fired", "node_id": node.id}

async def action_node_handler(node: Node, context: Dict[str, Any]) -> Any:
    # Simulate action execution
    await asyncio.sleep(0.01)
    print(f"Action {node.id} executed")
    return {"status": "success", "node_id": node.id}

NODE_REGISTRY = {
    "trigger": trigger_node_handler,
    "action": action_node_handler,
}
