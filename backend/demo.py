import asyncio
import aiohttp
import json

async def run_demo():
    print("🚀 Starting Visual Automation Builder Backend Demo...")
    
    workflow_payload = {
        "workflowId": "demo-1234",
        "name": "Demo Workflow",
        "nodes": [
            {
                "id": "node-trigger-1",
                "role": "trigger",
                "data": {"label": "GitHub Webhook", "role": "trigger"},
                "position": {"x": 100, "y": 100}
            },
            {
                "id": "node-action-1",
                "role": "action",
                "data": {"label": "Discord Notification", "role": "action"},
                "position": {"x": 400, "y": 100}
            }
        ],
        "edges": [
            {
                "id": "edge-1",
                "source": "node-trigger-1",
                "target": "node-action-1"
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        print("\n1️⃣  Testing Pydantic Workflow Validation & DAG Engine...")
        async with session.post('http://localhost:3001/api/workflows', json=workflow_payload) as response:
            result = await response.json()
            print(f"Status Code: {response.status}")
            print(f"Response: {json.dumps(result, indent=2)}")
            
        print("\n2️⃣  Running Webhook Ingestion Server Load Test...")
        import load_test
        await load_test.main()

if __name__ == "__main__":
    asyncio.run(run_demo())
