import axios from 'axios';
import CustomEdge from './CustomEdge';

import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState
} from 'reactflow';
import 'reactflow/dist/style.css';
import { nodeTypes } from './NodeTypes';

const initialNodes = [
  {
    id: '1',
    type: 'trigger',
    position: { x: 100, y: 100 },
    data: {
      label: 'GitHub Trigger',
      role: 'trigger'     // 🔑 ADD THIS
    }
  },
  {
    id: '2',
    type: 'action',
    position: { x: 400, y: 100 },
    data: {
      label: 'Discord Action',
      role: 'action'      // 🔑 ADD THIS
    }
  }
];

// const initialNodes = [
//   {
//     id: '1',
//     type: 'trigger',
//     position: { x: 100, y: 100 },
//     data: { label: 'GitHub Trigger' }
//   },
//   {
//     id: '2',
//     type: 'action',
//     position: { x: 400, y: 100 },
//     data: { label: 'Discord Action' }
//   }
// ];

const initialEdges = [];

export default function WorkflowCanvas() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

const onConnect = useCallback(
  (params) =>
    setEdges((eds) =>
      addEdge(
        {
          ...params,
          type: 'custom',
          animated: true,
          selectable: true,
        },
        eds
      )
    ),
  [setEdges]
);

const isValidConnection = (connection) => {
  const sourceNode = nodes.find(n => n.id === connection.source);
  const targetNode = nodes.find(n => n.id === connection.target);

  if (!sourceNode || !targetNode) return false;

  // Only Trigger → Action allowed
  return (
    sourceNode.data.role === 'trigger' &&
    targetNode.data.role === 'action'
  );
};


const serializeWorkflow = () => {
  return {
    workflowId: crypto.randomUUID(),
    name: 'Visual Automation Workflow',

    nodes: nodes.map((node) => ({
      id: node.id,

      // semantic role (engine)
      role: node.data.role,

      // render type (UI)
      renderType: node.type,

      position: node.position,
      data: node.data,
    })),

    edges: edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
    })),

    createdAt: new Date().toISOString(),
  };
};



// const serializeWorkflow = () => {
//     return {
//       workflowId: crypto.randomUUID(),
//       name: 'Visual Automation Workflow',
//       nodes: nodes.map((node) => ({
//         id: node.id,
      
//         // 🔑 SEMANTIC ROLE (engine)
//         role: node.data.role,  
      
//         // 🔑 RENDER TYPE (UI)
//         renderType: node.type,
      
//         position: node.position,
//         data: node.data
//       }))    
//       // nodes: nodes.map((node) => ({
//       //   id: node.id,
//       //   role: node.type,              // trigger | action
//       //   position: node.position,
//       //   data: node.data
//       // })),
//       // edges: edges.map((edge) => ({
//       //   id: edge.id,
//       //   source: edge.source,
//       //   target: edge.target
//       // })),
//       // createdAt: new Date().toISOString()
//     };
//   };
  
//   const memoizedNodeTypes = useMemo(() => nodeTypes, []);
    const memoizedNodeTypes = useMemo(
        () => ({
        ...nodeTypes
        }),
        []
    );

    // const onEdgeClick = useCallback((event, edge) => {
    //   event.stopPropagation();
    //   setEdges((eds) => eds.map(e =>
    //     e.id === edge.id ? { ...e, selected: true } : { ...e, selected: false }
    //   ));
    // }, [setEdges]);
    
    const edgeTypes = useMemo(
      () => ({
        custom: CustomEdge,
      }),
      []
    );
    
  


  return (
    <div style={{ height: '100vh' }}>
        
        <button  onClick={async () => {
          const workflow = serializeWorkflow();
          console.log('Serialized Workflow:', workflow);

          console.log(
          'EDGE DIRECTION DEBUG:',
          edges.map(e => `${e.source} -> ${e.target}`)
        );


          try {
            const response = await axios.post(
              'http://localhost:3001/api/workflows',
              workflow
            );

            alert('✅ Workflow validated and accepted');
            console.log('Backend response:', response.data);

          } catch (error) {
            if (error.response) {
              // Validation error from backend
              const errors = error.response.data.errors;
              alert('❌ Workflow validation failed:\n\n' + errors.join('\n'));
              console.error('Validation errors:', errors);
            } else {
              alert('❌ Network or server error');
              console.error(error);
            }
          }
        }}
        style={{
          position: 'absolute',
          zIndex: 10,
          top: 10,
          left: 10,
          padding: '8px 12px',
          background: '#111827',
          color: '#fff',
          borderRadius: 6
        }}
      >
        Serialize Workflow
        </button>

      <ReactFlow
          nodes={nodes}
          edges={edges}
          connectionMode="strict"
          nodeTypes={memoizedNodeTypes}
          edgeTypes={edgeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          isValidConnection={isValidConnection}
          fitView
          deleteKeyCode={['Backspace', 'Delete']}    
    >

        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
