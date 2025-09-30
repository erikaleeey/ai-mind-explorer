import { useState } from 'react';
import { Agent } from '../types';

export const useAgentAnalysis = () => {
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [agents, setAgents] = useState<Agent[]>([
    { id: 'aoi', name: 'AOI Agent', icon: '🎯', description: 'Define criteria buckets', active: false },
    { id: 'evidence', name: 'Evidence Extractor', icon: '🔍', description: 'Extract evidence', active: false },
    { id: 'verifier', name: 'Verifier Agent', icon: '✓', description: 'Validate mappings', active: false },
    { id: 'scoring', name: 'Scoring Agent', icon: '📊', description: 'Calculate scores', active: false }
  ]);

  const runAgentAnalysis = (addToLedger: (action: string) => void) => {
    addToLedger('Started multi-agent analysis');
    setAnalysisProgress(0);
    
    agents.forEach((agent, index) => {
      setTimeout(() => {
        setAgents(prev => prev.map(a => a.id === agent.id ? { ...a, active: true } : a));
        setAnalysisProgress((index + 1) * 25);
        
        if (index === agents.length - 1) {
          setTimeout(() => {
            setAgents(prev => prev.map(a => ({ ...a, active: false })));
            addToLedger('Multi-agent analysis completed');
          }, 1000);
        }
      }, (index + 1) * 1500);
    });
  };

  return { agents, analysisProgress, runAgentAnalysis };
};