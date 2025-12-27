async function triggerNode({ node, context }) {
    console.log(`🔔 Trigger fired: ${node.data.label}`);
  
    return {
      triggeredAt: new Date().toISOString(),
      message: `${node.data.label} triggered`,
    };
  }
  
  module.exports = triggerNode;
  