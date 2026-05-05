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
  url: string;
}

interface FeedStore {
  items: FeedItem[];
  briefing: string;
  loading: boolean;
  error: string | null;
  pipelineStatus: 'idle' | 'running' | 'success' | 'error';
  integrationStatus: { github: boolean, gmail: boolean, slack: boolean };
  fetchItems: (userId: number) => Promise<void>;
  fetchBriefing: (userId: number) => Promise<void>;
  fetchIntegrationStatus: (userId: number) => Promise<void>;
  triggerPipeline: (userId: number) => Promise<void>;
  clearError: () => void;
}

export const useFeedStore = create<FeedStore>((set, get) => ({
  items: [],
  briefing: '',
  loading: false,
  error: null,
  pipelineStatus: 'idle',
  integrationStatus: { github: false, gmail: false, slack: false },

  clearError: () => set({ error: null }),

  fetchItems: async (userId: number) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/feed/items/${userId}`);
      set({ items: response.data });
    } catch (error) {
      console.error('Failed to fetch items:', error);
    }
  },

  fetchBriefing: async (userId: number) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/feed/briefing/${userId}`);
      set({ briefing: response.data.content });
    } catch (error) {
      console.error('Failed to fetch briefing:', error);
    }
  },

  fetchIntegrationStatus: async (userId: number) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/status/${userId}`);
      set({ integrationStatus: response.data });
    } catch (error) {
      console.error('Failed to fetch integration status:', error);
    }
  },

  triggerPipeline: async (userId: number) => {
    set({ loading: true, error: null, pipelineStatus: 'running' });
    try {
      await axios.post(`${API_BASE_URL}/feed/trigger-pipeline/${userId}`);
      
      // Poll for results — the pipeline runs in background on the server
      // We check every 3 seconds up to 10 times (30 seconds max)
      let attempts = 0;
      const maxAttempts = 10;
      
      const poll = async () => {
        attempts++;
        try {
          const itemsRes = await axios.get(`${API_BASE_URL}/feed/items/${userId}`);
          const briefingRes = await axios.get(`${API_BASE_URL}/feed/briefing/${userId}`);
          
          const newItems = itemsRes.data;
          const newBriefing = briefingRes.data.content;
          const currentItems = get().items;
          
          // Check if data has changed (pipeline has finished)
          const hasNewData = newItems.length !== currentItems.length || 
            (newItems.length > 0 && currentItems.length > 0 && newItems[0]?.id !== currentItems[0]?.id);
          
          if (hasNewData || attempts >= maxAttempts) {
            set({ 
              items: newItems, 
              briefing: newBriefing, 
              loading: false, 
              pipelineStatus: hasNewData ? 'success' : 'success'
            });
            
            // Reset status after 3 seconds
            setTimeout(() => set({ pipelineStatus: 'idle' }), 3000);
          } else {
            // Keep polling
            setTimeout(poll, 3000);
          }
        } catch {
          if (attempts < maxAttempts) {
            setTimeout(poll, 3000);
          } else {
            set({ loading: false, pipelineStatus: 'error', error: 'Pipeline timed out. Please try again.' });
            setTimeout(() => set({ pipelineStatus: 'idle', error: null }), 5000);
          }
        }
      };
      
      // Start polling after an initial delay
      setTimeout(poll, 4000);
    } catch (error) {
      set({ 
        error: 'Failed to trigger pipeline. Check your connection.', 
        loading: false, 
        pipelineStatus: 'error' 
      });
      setTimeout(() => set({ pipelineStatus: 'idle', error: null }), 5000);
      console.error(error);
    }
  },
}));
