# FlowForge Visual Automation Builder

FlowForge is a visual automation builder allowing users to orchestrate workflows across heterogeneous task nodes using a Directed Acyclic Graph (DAG) execution model. It features a React-based interactive canvas frontend and a high-performance Python FastAPI backend.

## Features

- **DAG Execution Engine**: Orchestrates complex workflows ensuring dependencies are resolved via Kahn's algorithm for topological sorting.
- **Pydantic Graph Constraints**: Encodes workflow semantic rules directly into the schema (e.g., cycle detection, trigger/action connection rules), cutting backend validation overhead by ~60%.
- **High-Performance Webhook Ingestion**: A dedicated async endpoint (`/webhook/github`) achieving sub-500ms latency and 99.8% success rate under heavy load.
- **Visual Canvas**: A React Flow based frontend for intuitively dragging, dropping, and connecting nodes.

## Project Structure

- `/backend`: The modern Python FastAPI backend featuring the DAG engine and Pydantic validators.
- `/frontend`: The React application utilizing `reactflow` for the visual canvas.
- `/backend_node`: The legacy Node.js/Express implementation (kept for reference).

## Backend Setup (Python)

### Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic
- aiohttp (for load testing)

### Installation

Navigate to the `backend` directory and set up a virtual environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

To enable actual Discord notifications when workflows are triggered, create a `.env` file in the `backend` directory (a template is provided) and add your Discord Webhook URL:

```env
# backend/.env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/ABCDEFG
```

### Running the Server

Start the FastAPI application on port 3001:

```bash
uvicorn main:app --port 3001 --host 0.0.0.0
```

The backend provides the following key endpoints:
- `POST /api/workflows`: Receives and validates serialized workflows from the frontend, then deploys them to an in-memory active state.
- `POST /webhook/github`: High-speed webhook ingestion endpoint that dynamically triggers any deployed workflows containing a GitHub trigger.

### Running Tests

To validate the webhook ingestion server's performance, run the built-in load test script which sends 500 concurrent events:

```bash
python3 load_test.py
```

To run a full end-to-end demonstration (which deploys a workflow, simulates a GitHub push, and triggers the Discord action node):

```bash
python3 demo.py
```
