import { create } from 'zustand';

export interface Rule {
  id: string;
  title: string;
  description: string;
}

interface RuleState {
  rules: Rule[];
  setRules: (rules: Rule[]) => void;
  addRule: (rule: Rule) => void;
  updateRule: (id: string, updatedRule: Rule) => void;
  removeRule: (id: string) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

export const useRuleStore = create<RuleState>((set) => ({
  rules: [],
  setRules: (rules) => set({ rules }),
  addRule: (rule) => set((state) => ({ rules: [...state.rules, rule] })),
  updateRule: (id, updatedRule) => set((state) => ({
    rules: state.rules.map(r => r.id === id ? updatedRule : r)
  })),
  removeRule: (id) => set((state) => ({ rules: state.rules.filter(r => r.id !== id) })),
  loading: false,
  setLoading: (loading) => set({ loading })
}));
