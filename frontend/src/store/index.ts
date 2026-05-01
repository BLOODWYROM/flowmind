import { create } from 'zustand';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface FeedItem {
  id: number;
  user_id: number;
  external_id: string;
  tool_name: string;
  title: string;
  content: string;
  author: string;
  priority_score: number;
  priority_tag: string;
  ai_explanation: string;
  timestamp: string;
}

interface FeedStore {
  items: FeedItem[];
  briefing: string;
  loading: boolean;
  error: string | null;
  fetchItems: (userId: number) => Promise<void>;
  fetchBriefing: (userId: number) => Promise<void>;
  triggerPipeline: (userId: number) => Promise<void>;
}

export const useFeedStore = create<FeedStore>((set) => ({
  items: [],
  briefing: '',
  loading: false,
  error: null,

  fetchItems: async (userId: number) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/feed/items/${userId}`);
      set({ items: response.data, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch items', loading: false });
      console.error(error);
    }
  },

  fetchBriefing: async (userId: number) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/feed/briefing/${userId}`);
      set({ briefing: response.data.content, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch briefing', loading: false });
      console.error(error);
    }
  },

  triggerPipeline: async (userId: number) => {
    set({ loading: true, error: null });
    try {
      await axios.post(`${API_BASE_URL}/feed/trigger-pipeline/${userId}`);
      // The pipeline runs in the background. In a real app, we might use WebSockets or polling.
      // For now, we'll just wait a bit and fetch the items.
      setTimeout(async () => {
        const { fetchItems, fetchBriefing } = useFeedStore.getState();
        await fetchItems(userId);
        await fetchBriefing(userId);
        set({ loading: false });
      }, 5000); // Polling delay
    } catch (error) {
      set({ error: 'Failed to trigger pipeline', loading: false });
      console.error(error);
    }
  },
}));
