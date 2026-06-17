// async function actionNode({ node, context }) {
//     console.log(`⚙️ Executing action: ${node.data.label}`);
//     console.log('📦 Input context:', context);
  
//     return {
//       executedAt: new Date().toISOString(),
//       message: `${node.data.label} executed`,
//     };
//   }
  
//   module.exports = actionNode;
  
const axios = require('axios');

async function actionNode({ input }) {
  const webhook = process.env.DISCORD_WEBHOOK_URL;

  if (!webhook) {
    throw new Error('DISCORD_WEBHOOK_URL not set');
  }

  const message = {
    content: `🚀 New GitHub push to **${input.repo}**
👤 Pusher: ${input.pusher}
📦 Commits: ${input.commits}`,
  };

  await axios.post(webhook, message);

  console.log('📤 Sent message to Discord');

  return { sent: true };
}

module.exports = actionNode;
