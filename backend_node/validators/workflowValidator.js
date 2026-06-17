// function validateWorkflow(workflow) {
//     const errors = [];
  
//     if (!workflow.nodes || workflow.nodes.length === 0) {
//       errors.push('Workflow must contain nodes');
//       return errors;
//     }
  
//     const triggers = workflow.nodes.filter(n => n.role === 'trigger');
//     const actions = workflow.nodes.filter(n => n.role === 'action');
  
//     if (triggers.length === 0) {
//       errors.push('Workflow must contain at least one trigger');
//     }
  
//     if (actions.length === 0) {
//       errors.push('Workflow must contain at least one action');
//     }
  
//     if (!workflow.edges || workflow.edges.length === 0) {
//       errors.push('Workflow must contain at least one connection (edge)');
//     }
  
//     // Ensure each action has an incoming edge
//     const actionIds = new Set(actions.map(a => a.id));
//     const connectedActionIds = new Set(workflow.edges.map(e => e.target));
  
//     actionIds.forEach(actionId => {
//       if (!connectedActionIds.has(actionId)) {
//         errors.push(`Action node ${actionId} has no incoming connection`);
//       }
//     });
  
//     return errors;
//   }
  
//   module.exports = { validateWorkflow };
  
function validateWorkflow(workflow) {
    const errors = [];
  
    if (!workflow.nodes || workflow.nodes.length === 0) {
      errors.push('Workflow must contain nodes');
      return errors;
    }
  
    const nodesById = new Map();
    workflow.nodes.forEach((node) => {
      nodesById.set(node.id, node);
    });
  
    const triggers = workflow.nodes.filter((n) => n.role === 'trigger');
    const actions = workflow.nodes.filter((n) => n.role === 'action');
  
    if (triggers.length === 0) {
      errors.push('Workflow must contain at least one trigger');
    }
  
    if (actions.length === 0) {
      errors.push('Workflow must contain at least one action');
    }
  
    if (!workflow.edges || workflow.edges.length === 0) {
      errors.push('Workflow must contain at least one connection (edge)');
      return errors;
    }
  
    // --- Semantic edge validation ---
    workflow.edges.forEach((edge) => {
      const sourceNode = nodesById.get(edge.source);
      const targetNode = nodesById.get(edge.target);

      console.log(
        `Edge ${edge.source} -> ${edge.target}`,
        'source role:', sourceNode.role,
        'target role:', targetNode.role
      );
      
  
      if (!sourceNode || !targetNode) {
        errors.push(`Edge ${edge.id} references invalid node`);
        return;
      }
  
      // Rule 1: Triggers cannot have incoming edges
      if (targetNode.role === 'trigger') {
        errors.push(
          `Invalid connection: trigger node "${targetNode.id}" cannot have incoming edges`
        );
      }
  
      // Rule 2: Actions cannot be sources for triggers
      if (sourceNode.role === 'action' && targetNode.role === 'trigger') {
        errors.push(
          `Invalid connection: action "${sourceNode.id}" cannot connect to trigger "${targetNode.id}"`
        );
      }
  
      // Rule 3: Trigger → Trigger is invalid
      if (sourceNode.role === 'trigger' && targetNode.role === 'trigger') {
        errors.push(
          `Invalid connection: trigger "${sourceNode.id}" cannot connect to trigger "${targetNode.id}"`
        );
      }
    });
  
    // --- Ensure every action has at least one incoming edge ---
    const actionIds = new Set(actions.map((a) => a.id));
    const connectedTargets = new Set(workflow.edges.map((e) => e.target));
  
    actionIds.forEach((actionId) => {
      if (!connectedTargets.has(actionId)) {
        errors.push(`Action node "${actionId}" has no incoming connection`);
      }
    });
  
    return errors;
  }
  
  module.exports = { validateWorkflow };
  