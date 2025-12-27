import { Handle, Position } from 'reactflow';

export const TriggerNode = ({ data }) => (
  <div
    style={{
      border: '2px solid #3b82f6',
      borderRadius: 8,
      padding: 12,
      background: 'white',
      minWidth: 160,
    }}
  >
    <strong>Trigger</strong>
    <div>{data.label}</div>

    {/* ONLY outgoing */}
    <Handle
      type="source"
      position={Position.Right}
      id="trigger-out"
    />
  </div>
);

export const ActionNode = ({ data }) => (
  <div
    style={{
      border: '2px solid #22c55e',
      borderRadius: 8,
      padding: 12,
      background: 'white',
      minWidth: 160,
    }}
  >
    <strong>Action</strong>
    <div>{data.label}</div>

    {/* ONLY incoming */}
    <Handle
      type="target"
      position={Position.Left}
      id="action-in"
    />
  </div>
);
export const nodeTypes = {
  trigger: TriggerNode,
  action: ActionNode,
};

