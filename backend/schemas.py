from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Any, Optional

class NodeData(BaseModel):
    label: str
    role: str
    # any other fields in data...
    model_config = {"extra": "allow"}

class Position(BaseModel):
    x: float
    y: float

class Node(BaseModel):
    id: str
    role: str
    renderType: Optional[str] = None
    position: Optional[Position] = None
    data: NodeData
    
    @model_validator(mode='after')
    def check_roles(self):
        if self.role != self.data.role:
            raise ValueError(f"Role mismatch: node role '{self.role}' vs data role '{self.data.role}'")
        return self

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Workflow(BaseModel):
    workflowId: str
    name: str = "Workflow"
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)
    createdAt: Optional[str] = None

    @model_validator(mode='after')
    def validate_graph_constraints(self) -> 'Workflow':
        errors = []
        
        if not self.nodes:
            raise ValueError("Workflow must contain nodes")
            
        triggers = [n for n in self.nodes if n.role == "trigger"]
        actions = [n for n in self.nodes if n.role == "action"]
        
        if not triggers:
            errors.append("Workflow must contain at least one trigger")
        if not actions:
            errors.append("Workflow must contain at least one action")
            
        if not self.edges:
            raise ValueError("Workflow must contain at least one connection (edge)")
            
        nodes_by_id = {n.id: n for n in self.nodes}
        
        # Track incoming edges for actions
        connected_targets = {e.target for e in self.edges}
        
        for edge in self.edges:
            source_node = nodes_by_id.get(edge.source)
            target_node = nodes_by_id.get(edge.target)
            
            if not source_node or not target_node:
                errors.append(f"Edge {edge.id} references invalid node")
                continue
                
            # Rule 1: Triggers cannot have incoming edges
            if target_node.role == 'trigger':
                errors.append(f"Invalid connection: trigger node '{target_node.id}' cannot have incoming edges")
                
            # Rule 2: Actions cannot be sources for triggers
            if source_node.role == 'action' and target_node.role == 'trigger':
                errors.append(f"Invalid connection: action '{source_node.id}' cannot connect to trigger '{target_node.id}'")
                
            # Rule 3: Trigger -> Trigger is invalid
            if source_node.role == 'trigger' and target_node.role == 'trigger':
                errors.append(f"Invalid connection: trigger '{source_node.id}' cannot connect to trigger '{target_node.id}'")
                
        # Ensure every action has an incoming edge
        for action in actions:
            if action.id not in connected_targets:
                errors.append(f"Action node '{action.id}' has no incoming connection")
                
        # Cycle Detection (Kahn's algorithm check)
        in_degree = {n.id: 0 for n in self.nodes}
        graph = {n.id: [] for n in self.nodes}
        
        for edge in self.edges:
            if edge.source in graph and edge.target in in_degree:
                graph[edge.source].append(edge.target)
                in_degree[edge.target] += 1
                
        queue = [n_id for n_id, deg in in_degree.items() if deg == 0]
        visited_count = 0
        
        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for neighbor in graph[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if visited_count != len(self.nodes):
            errors.append("Workflow contains a cycle")

        if errors:
            raise ValueError(" | ".join(errors))
            
        return self
