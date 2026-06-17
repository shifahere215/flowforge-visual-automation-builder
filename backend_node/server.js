require('dotenv').config();
const { topologicalSort } = require('./engine/topologicalSort');
const { executeWorkflow } = require('./engine/executeWorkflow');
const { validateWorkflow } = require('./validators/workflowValidator');
const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(express.json());

// --- TEMP STORAGE (in-memory) ---
const workflows = [];

app.post('/webhook/github', async (req, res) => {
  console.log('📩 GitHub webhook received');

  const eventType = req.headers['x-github-event'];
  const payload = req.body;

  global.latestGitHubEvent = {
    event: eventType,
    repo: payload.repository?.full_name,
    pusher: payload.pusher?.name,
    commits: payload.commits?.length || 0,
    timestamp: new Date().toISOString(),
  };

  console.log('Stored GitHub event:', global.latestGitHubEvent);

  res.status(200).json({ received: true });
});



// --- Receive workflow JSON ---
app.post('/api/workflows', async(req, res) => {
    const workflow = req.body;
  
    const errors = validateWorkflow(workflow);
  
    if (errors.length > 0) {
      console.error('❌ Workflow validation failed:', errors);
      return res.status(400).json({
        success: false,
        errors
      });
    }

    const executionOrder = topologicalSort(workflow.nodes, workflow.edges);

    console.log('🧭 Execution order:', executionOrder);


    // --- NEW EXECUTION LOGIC START ---
    // 2. We 'await' the result because execution takes time (API calls, scraping, etc.)
    const executionResult = await executeWorkflow(workflow, executionOrder);

    res.status(200).json({
        success: true,
        message: 'Workflow executed successfully',
        workflowId: workflow.workflowId,
        executionOrder,
        executionResult
    });

  
    // console.log('✅ Valid workflow received:');
    // console.dir(workflow, { depth: null });
  
    // res.status(200).json({
    //   success: true,
    //   message: 'Workflow validated and accepted',
    //   workflowId: workflow.workflowId
    // });
  });
  

// --- Health check ---
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 Backend running on http://localhost:${PORT}`);
});
