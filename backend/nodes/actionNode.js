async function actionNode({ node, context }) {
    console.log(`⚙️ Executing action: ${node.data.label}`);
    console.log('📦 Input context:', context);
  
    return {
      executedAt: new Date().toISOString(),
      message: `${node.data.label} executed`,
    };
  }
  
  module.exports = actionNode;
  