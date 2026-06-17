from fastapi import APIRouter, HTTPException
from schemas import Workflow
from engine.dag import topological_sort, execute_workflow

router = APIRouter()

@router.post("/workflows")
async def receive_workflow(workflow: Workflow):
    # If the execution reaches here, Pydantic validation has passed.
    try:
        execution_order = topological_sort(workflow)
        print("🧭 Execution order:", execution_order)
        
        execution_result = await execute_workflow(workflow, execution_order)
        
        return {
            "success": True,
            "message": "Workflow executed successfully",
            "workflowId": workflow.workflowId,
            "executionOrder": execution_order,
            "executionResult": execution_result
        }
    except ValueError as e:
        # Catch errors like cycles (which we might also catch in Pydantic, but just in case)
        raise HTTPException(status_code=400, detail={"success": False, "errors": [str(e)]})
