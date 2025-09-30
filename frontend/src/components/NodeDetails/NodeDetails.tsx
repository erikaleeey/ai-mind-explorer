import React from 'react';
import { ThoughtNode } from '../../types/reasoning';
import './NodeDetails.css';

interface NodeDetailsProps {
  node: ThoughtNode | null;
  onClose: () => void;
}

export const NodeDetails: React.FC<NodeDetailsProps> = ({ node, onClose }) => {
  if (!node) return null;

  const typeColors: Record<string, string> = {
    question: '#3b82f6',
    retrieval: '#10b981',
    reasoning: '#f59e0b',
    conclusion: '#ef4444'
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="node-type-badge" style={{ backgroundColor: typeColors[node.type] }}>
            {node.type.toUpperCase()}
          </div>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          <div className="detail-section">
            <h3>Thought Content</h3>
            <p className="thought-content">{node.content}</p>
          </div>

          <div className="detail-section">
            <h3>Confidence Level</h3>
            <div className="confidence-bar-container">
              <div
                className="confidence-bar"
                style={{
                  width: `${node.confidence * 100}%`,
                  backgroundColor: typeColors[node.type]
                }}
              />
            </div>
            <p className="confidence-text">{Math.round(node.confidence * 100)}%</p>
          </div>

          <div className="detail-section">
            <h3>Node Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">ID:</span>
                <span className="info-value">{node.id}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Session:</span>
                <span className="info-value">{node.session_id}</span>
              </div>
            </div>
          </div>

          <div className="phase-notice">
            <p>🚀 <strong>Coming in Phase 2:</strong> Edit this node's content and watch the reasoning chain update in real-time!</p>
          </div>
        </div>
      </div>
    </div>
  );
};
