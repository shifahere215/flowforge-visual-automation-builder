// async function triggerNode({ node, context }) {
//     console.log(`🔔 Trigger fired: ${node.data.label}`);
  
//     return {
//       triggeredAt: new Date().toISOString(),
//       message: `${node.data.label} triggered`,
//     };
//   }
  
//   module.exports = triggerNode;
  

async function triggerNode() {
  if (!global.latestGitHubEvent) {
    throw new Error('No GitHub event received yet');
  }

  console.log('🔔 Trigger fired from GitHub event');

  return global.latestGitHubEvent;
}

module.exports = triggerNode;

