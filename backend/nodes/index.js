const triggerNode = require('./triggerNode');
const actionNode = require('./actionNode');

const nodeRegistry = {
  trigger: triggerNode,
  action: actionNode,
};

module.exports = { nodeRegistry };
