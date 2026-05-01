import { create } from 'zustand'

export interface Item {
  id: number;
  tool_name: string;
  title: string;
  content: string;
  url: string;
  author: string;
  timestamp: string;
  priority_score: number;
  priority_tag: string;
  ai_explanation: string;
}

interface AppState {
  userId: number;
  userEmail: string;
  items: Item[];
  briefing: string;
  integrations: {
    github: boolean;
    gmail: boolean;
  };
  setUserId: (id: number, email: string) => void;
  setItems: (items: Item[]) => void;
  setBriefing: (briefing: string) => void;
  setIntegrations: (status: { github: boolean, gmail: boolean }) => void;
}

export const useStore = create<AppState>((set) => ({
  userId: 1, // default mock user
  userEmail: 'dev@example.com',
  items: [],
  briefing: '',
  integrations: {
    github: false,
    gmail: false,
  },
  setUserId: (id, email) => set({ userId: id, userEmail: email }),
  setItems: (items) => set({ items }),
  setBriefing: (briefing) => set({ briefing }),
  setIntegrations: (status) => set({ integrations: status }),
}))
