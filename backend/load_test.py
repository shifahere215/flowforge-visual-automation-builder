import asyncio
import aiohttp
import time
import statistics

async def send_webhook(session, url, payload, headers):
    start_time = time.perf_counter()
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            await response.read()
            end_time = time.perf_counter()
            return response.status, (end_time - start_time) * 1000
    except Exception as e:
        end_time = time.perf_counter()
        return str(e), (end_time - start_time) * 1000

async def main():
    url = "http://localhost:3001/webhook/github"
    num_requests = 500
    
    payload = {
        "repository": {"full_name": "user/repo"},
        "pusher": {"name": "test_user"},
        "commits": [{"id": "1"}, {"id": "2"}]
    }
    headers = {"x-github-event": "push"}
    
    print(f"Starting load test: sending {num_requests} concurrent webhook events...")
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_webhook(session, url, payload, headers) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        
    successes = 0
    failures = 0
    latencies = []
    
    for status, latency in results:
        latencies.append(latency)
        if status == 200:
            successes += 1
        else:
            failures += 1
            
    success_rate = (successes / num_requests) * 100
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    
    print("\n--- Load Test Results ---")
    print(f"Total Requests : {num_requests}")
    print(f"Successes      : {successes}")
    print(f"Failures       : {failures}")
    print(f"Success Rate   : {success_rate:.2f}%")
    print(f"Min Latency    : {min_latency:.2f} ms")
    print(f"Avg Latency    : {avg_latency:.2f} ms")
    print(f"Max Latency    : {max_latency:.2f} ms")
    
    if success_rate >= 99.8 and max_latency <= 500:
        print("\n✅ Load test PASSED: Sub-500ms latency and >= 99.8% success rate achieved.")
    else:
        print("\n❌ Load test FAILED to meet requirements.")

if __name__ == "__main__":
    asyncio.run(main())
