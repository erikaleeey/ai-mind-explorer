import { useState } from 'react';
import { CSO, Vendor } from '../types';

export const useVendorData = () => {
  // Sample data - replace with API calls in production
  const [csos] = useState<CSO[]>([
    { id: '1', name: 'AI/ML Solutions', description: 'Advanced machine learning and artificial intelligence applications', vendorCount: 24, phase2Count: 8, progress: 85 },
    { id: '2', name: 'Cybersecurity', description: 'Next-generation security solutions and threat detection', vendorCount: 18, phase2Count: 5, progress: 62 },
    { id: '3', name: 'Quantum Computing', description: 'Quantum algorithms and hardware solutions', vendorCount: 12, phase2Count: 3, progress: 45 }
  ]);

  const [vendors] = useState<Vendor[]>([
    { id: 'v1', name: 'TechCorp AI', score: 92, status: 'approved', brief: 'Advanced NLP solution', phase: 1 },
    { id: 'v2', name: 'QuantumSoft', score: 87, status: 'approved', brief: 'Quantum ML algorithms', phase: 1 },
    { id: 'v3', name: 'NeuralNet Inc', score: 78, status: 'pending', brief: 'Deep learning platform', phase: 1 },
    { id: 'v4', name: 'DataMinds', score: 65, status: 'pending', brief: 'Data analytics suite', phase: 1 },
    { id: 'v5', name: 'AIVision', score: 45, status: 'rejected', brief: 'Computer vision tools', phase: 1 },
    { id: 'v6', name: 'CyberShield', score: 88, status: 'approved', brief: 'AI-powered security', phase: 2 }
  ]);

  // In production, replace with actual API calls:
  // const fetchVendors = async (csoId: string) => {
  //   const response = await fetch(`/api/vendors/${csoId}`);
  //   return response.json();
  // };

  return { csos, vendors };
};