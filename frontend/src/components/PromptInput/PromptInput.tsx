import React, { useState } from 'react';
import './PromptInput.css';

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  loading?: boolean;
}

export const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, loading = false }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !loading) {
      onSubmit(prompt.trim());
    }
  };

  const examplePrompts = [
    "Why is the sky blue?",
    "How does photosynthesis work?",
    "What causes earthquakes?",
    "Explain quantum entanglement"
  ];

  return (
    <div className="prompt-input-container">
      <h2>Ask a Question</h2>
      <p className="subtitle">Watch the AI's reasoning process unfold as a live graph</p>

      <form onSubmit={handleSubmit} className="prompt-form">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask anything... e.g., 'Why is the sky blue?'"
          disabled={loading}
          rows={4}
        />

        <button type="submit" disabled={!prompt.trim() || loading}>
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating Reasoning...
            </>
          ) : (
            '🧠 Explore Reasoning'
          )}
        </button>
      </form>

      <div className="example-prompts">
        <p>Try these examples:</p>
        <div className="examples-grid">
          {examplePrompts.map((example, idx) => (
            <button
              key={idx}
              className="example-btn"
              onClick={() => setPrompt(example)}
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
