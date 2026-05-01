"use client";

import { useStore } from '../lib/store';
import { Sparkles, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { useState } from 'react';

export default function MorningBriefing() {
  const { briefing, userId, setBriefing, setItems } = useStore();
  const [loading, setLoading] = useState(false);

  const handleRefresh = async () => {
    setLoading(true);
    try {
      // Trigger background pipeline
      await axios.post(`http://localhost:8000/api/feed/trigger-pipeline/${userId}`);
      
      // Poll for results after a few seconds (mocking real-time for MVP)
      setTimeout(async () => {
        const briefingRes = await axios.get(`http://localhost:8000/api/feed/briefing/${userId}`);
        const itemsRes = await axios.get(`http://localhost:8000/api/feed/items/${userId}`);
        
        setBriefing(briefingRes.data.content);
        setItems(itemsRes.data);
        setLoading(false);
      }, 5000);
      
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-blue-900/40 to-purple-900/40 border border-blue-500/20 rounded-xl p-6 relative overflow-hidden shadow-2xl">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <Sparkles size={120} />
      </div>
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="bg-blue-500/20 p-2 rounded-lg">
              <Sparkles className="text-blue-400" size={20} />
            </div>
            <h2 className="text-lg font-semibold text-blue-100">Morning Briefing</h2>
          </div>
          
          <button 
            onClick={handleRefresh}
            disabled={loading}
            className={`flex items-center gap-2 text-xs bg-white/5 hover:bg-white/10 px-3 py-1.5 rounded-full transition border border-white/10 text-gray-300 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            {loading ? 'Running Agents...' : 'Sync Now'}
          </button>
        </div>

        <p className="text-gray-300 leading-relaxed text-sm">
          {briefing || "Click 'Sync Now' to have your AI agents fetch, prioritize, and summarize your notifications from GitHub and Gmail."}
        </p>
      </div>
    </div>
  );
}
