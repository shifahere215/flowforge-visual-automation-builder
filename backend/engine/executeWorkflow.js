const { nodeRegistry } = require('../nodes');

async function executeWorkflow(workflow, executionOrder) {
  const context = {};

  for (const nodeId of executionOrder) {
    const node = workflow.nodes.find(n => n.id === nodeId);

    const handler = nodeRegistry[node.role];

    if (!handler) {
      throw new Error(`No handler registered for node role: ${node.role}`);
    }

    console.log(`▶️ Running node ${node.id} (${node.role})`);

    const output = await handler({ node, context });

    context[node.id] = output;
  }

  return context;
}

module.exports = { executeWorkflow };
