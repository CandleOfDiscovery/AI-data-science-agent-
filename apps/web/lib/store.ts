import { create } from 'zustand';

export type AgentState = {
  dataset?: unknown;
  analysis?: unknown;
  cleaning_plan: unknown[];
  charts: unknown[];
  report?: unknown;
  jobs: unknown[];
  setAnalysis: (analysis: unknown) => void;
};

export const useAgentStore = create<AgentState>((set) => ({
  cleaning_plan: [],
  charts: [],
  jobs: [],
  setAnalysis: (analysis) => set({ analysis }),
}));
