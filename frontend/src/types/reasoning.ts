export type ThoughtType = 'question' | 'retrieval' | 'reasoning' | 'conclusion';

export interface ThoughtNode {
  id: string;
  type: ThoughtType;
  content: string;
  confidence: number;
  session_id: string;
  metadata?: Record<string, any>;
  created_at?: string;
  // D3-specific properties (added by force simulation)
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;
}

export interface ReasoningEdge {
  source_id: string;
  target_id: string;
  label: string;
  confidence?: number;
  // D3-specific properties
  source?: ThoughtNode | string;
  target?: ThoughtNode | string;
}

export interface ReasoningChain {
  session_id: string;
  prompt: string;
  nodes: ThoughtNode[];
  edges: ReasoningEdge[];
  status: string;
  created_at?: string;
  metadata?: Record<string, any>;
}

export interface ProcessPromptRequest {
  prompt: string;
}
