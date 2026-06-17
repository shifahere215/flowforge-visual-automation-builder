from typing import List, Dict, Any
from schemas import Workflow
from engine.nodes import NODE_REGISTRY

def topological_sort(workflow: Workflow) -> List[str]:
    # Kahn's algorithm for topological sorting
    in_degree = {n.id: 0 for n in workflow.nodes}
    graph = {n.id: [] for n in workflow.nodes}
    
    for edge in workflow.edges:
        if edge.source in graph and edge.target in in_degree:
            graph[edge.source].append(edge.target)
            in_degree[edge.target] += 1
            
    queue = [n_id for n_id, deg in in_degree.items() if deg == 0]
    execution_order = []
    
    while queue:
        curr = queue.pop(0)
        execution_order.append(curr)
        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(execution_order) != len(workflow.nodes):
        raise ValueError("Workflow contains a cycle")
        
    return execution_order

async def execute_workflow(workflow: Workflow, execution_order: List[str], initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
    context: Dict[str, Any] = initial_context or {}
    
    nodes_by_id = {n.id: n for n in workflow.nodes}
    
    for node_id in execution_order:
        node = nodes_by_id[node_id]
        handler = NODE_REGISTRY.get(node.role)
        
        if not handler:
            raise ValueError(f"No handler registered for node role: {node.role}")
            
        print(f"▶️ Running node {node.id} ({node.role})")
        output = await handler(node, context)
        context[node.id] = output
        
    return context
