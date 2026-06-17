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
        print("\n1️⃣  Deploying Workflow...")
        async with session.post('http://localhost:3001/api/workflows', json=workflow_payload) as response:
            result = await response.json()
            print(f"Status Code: {response.status}")
            print(f"Response: {json.dumps(result, indent=2)}")
            
        print("\n2️⃣  Simulating GitHub Webhook...")
        github_payload = {
            "repository": {"full_name": "shifahere215/visual_automation"},
            "pusher": {"name": "kagakoko"},
            "commits": [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        }
        headers = {"x-github-event": "push"}
        async with session.post('http://localhost:3001/webhook/github', json=github_payload, headers=headers) as response:
            result = await response.json()
            print(f"Webhook response: {json.dumps(result)}")
            
        # Wait a moment for background task to execute
        await asyncio.sleep(1)
        
        print("\n3️⃣  Running Webhook Ingestion Server Load Test...")
        import load_test
        await load_test.main()

if __name__ == "__main__":
    asyncio.run(run_demo())
