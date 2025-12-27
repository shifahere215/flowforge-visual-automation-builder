function topologicalSort(nodes, edges) {
    const graph = new Map();
    const inDegree = new Map();
  
    // Initialize graph
    nodes.forEach(node => {
      graph.set(node.id, []);
      inDegree.set(node.id, 0);
    });
  
    // Build graph
    edges.forEach(edge => {
      graph.get(edge.source).push(edge.target);
      inDegree.set(edge.target, inDegree.get(edge.target) + 1);
    });
  
    // Collect nodes with no incoming edges
    const queue = [];
    inDegree.forEach((degree, nodeId) => {
      if (degree === 0) queue.push(nodeId);
    });
  
    const executionOrder = [];
  
    while (queue.length > 0) {
      const current = queue.shift();
      executionOrder.push(current);
  
      graph.get(current).forEach(neighbor => {
        inDegree.set(neighbor, inDegree.get(neighbor) - 1);
        if (inDegree.get(neighbor) === 0) {
          queue.push(neighbor);
        }
      });
    }
  
    // Cycle detection
    if (executionOrder.length !== nodes.length) {
      throw new Error('Workflow contains a cycle');
    }
  
    return executionOrder;
  }
  
  module.exports = { topologicalSort };
  