import { useState } from 'react';
import { LedgerEntry, User } from '../types';
import { generateHash } from '../utils/hash';

export const useLedger = () => {
  const [ledger, setLedger] = useState<LedgerEntry[]>([]);

  const addToLedger = (action: string, user?: User | null) => {
    const timestamp = new Date().toISOString();
    const hash = generateHash(action + timestamp);
    const entry: LedgerEntry = {
      timestamp,
      action,
      user: user?.role || 'System',
      hash
    };
    setLedger(prev => [entry, ...prev]);
  };

  return { ledger, addToLedger };
};