from fastapi import APIRouter, HTTPException
from schemas import Workflow
from engine.dag import topological_sort, execute_workflow

router = APIRouter()

DEPLOYED_WORKFLOWS = {}

@router.post("/workflows")
async def receive_workflow(workflow: Workflow):
    # If the execution reaches here, Pydantic validation has passed.
    try:
        # Pre-compute execution order and save to deployed workflows
        execution_order = topological_sort(workflow)
        
        DEPLOYED_WORKFLOWS[workflow.workflowId] = {
            "workflow": workflow,
            "execution_order": execution_order
        }
        
        print(f"✅ Workflow {workflow.workflowId} deployed successfully. Waiting for triggers...")
        
        return {
            "success": True,
            "message": "Workflow deployed and ready to trigger",
            "workflowId": workflow.workflowId,
            "executionOrder": execution_order,
        }
    except ValueError as e:
        # Catch errors like cycles (which we might also catch in Pydantic, but just in case)
        raise HTTPException(status_code=400, detail={"success": False, "errors": [str(e)]})
