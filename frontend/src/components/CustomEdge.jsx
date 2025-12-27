import { BaseEdge, getBezierPath } from 'reactflow';

export default function CustomEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  markerEnd,
}) {
  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  return (
    <BaseEdge
      id={id}                 // 🔑 REQUIRED
      path={edgePath}
      markerEnd={markerEnd}
      style={{
        stroke: '#2563eb',
        strokeWidth: 2,
        pointerEvents: 'all',  // 🔑 REQUIRED
      }}
      interactionWidth={20}   // 🔑 REQUIRED
    />
  );
}
