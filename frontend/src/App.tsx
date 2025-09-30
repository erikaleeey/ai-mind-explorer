import React, { useState } from 'react';
import axios from 'axios';
import { PromptInput } from './components/PromptInput/PromptInput';
import { ThoughtGraph } from './components/ThoughtGraph/ThoughtGraph';
import { NodeDetails } from './components/NodeDetails/NodeDetails';
import { ReasoningChain, ThoughtNode } from './types/reasoning';
import './styles/globals.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(false);
  const [reasoningChain, setReasoningChain] = useState<ReasoningChain | null>(null);
  const [selectedNode, setSelectedNode] = useState<ThoughtNode | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePromptSubmit = async (prompt: string) => {
    setLoading(true);
    setError(null);
    setReasoningChain(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/reasoning/process`, {
        prompt
      });

      setReasoningChain(response.data);
    } catch (err: any) {
      console.error('Error processing prompt:', err);

      if (err.response?.status === 500 && err.response?.data?.detail?.includes('OpenAI API key')) {
        setError('⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.');
      } else {
        setError('Failed to process prompt. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = (node: ThoughtNode) => {
    setSelectedNode(node);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧠 AI Mind Explorer</h1>
        <p>Visualize and interact with AI reasoning processes</p>
      </header>

      <main className="app-main">
        <PromptInput onSubmit={handlePromptSubmit} loading={loading} />

        {error && (
          <div className="error-banner">
            <p>{error}</p>
            {error.includes('API key') && (
              <div className="error-help">
                <p><strong>Quick fix:</strong></p>
                <ol>
                  <li>Copy <code>.env.example</code> to <code>.env</code></li>
                  <li>Add your OpenAI API key: <code>OPENAI_API_KEY=sk-your-key-here</code></li>
                  <li>Restart the backend server</li>
                </ol>
              </div>
            )}
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Generating reasoning chain...</p>
            <p className="loading-subtitle">Asking the AI to think step-by-step</p>
          </div>
        )}

        {reasoningChain && !loading && (
          <div className="reasoning-result">
            <div className="result-header">
              <h2>Reasoning Chain</h2>
              <div className="result-meta">
                <span>📝 Prompt: {reasoningChain.prompt}</span>
                <span>🔗 {reasoningChain.nodes.length} thought nodes</span>
                <span>⏱️ Session: {reasoningChain.session_id.slice(0, 8)}</span>
              </div>
            </div>

            <ThoughtGraph
              nodes={reasoningChain.nodes}
              edges={reasoningChain.edges}
              onNodeClick={handleNodeClick}
            />
          </div>
        )}

        {!loading && !reasoningChain && !error && (
          <div className="welcome-state">
            <h3>👋 Welcome to AI Mind Explorer!</h3>
            <p>Enter a question above to see how the AI reasons through it step-by-step.</p>
            <div className="features">
              <div className="feature">
                <span className="feature-icon">🎨</span>
                <h4>Visual Reasoning</h4>
                <p>See thoughts as an interactive graph</p>
              </div>
              <div className="feature">
                <span className="feature-icon">🔍</span>
                <p>Click nodes to explore</p>
              </div>
              <div className="feature">
                <span className="feature-icon">⚡</span>
                <h4>Real-time Generation</h4>
                <p>Watch reasoning unfold live</p>
              </div>
            </div>
          </div>
        )}
      </main>

      <NodeDetails node={selectedNode} onClose={() => setSelectedNode(null)} />
    </div>
  );
}

export default App;
