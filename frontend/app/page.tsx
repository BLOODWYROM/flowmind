"use client";

import Sidebar from '../components/Sidebar';
import MorningBriefing from '../components/MorningBriefing';
import UnifiedFeed from '../components/UnifiedFeed';
import { useEffect } from 'react';
import { useStore } from '../lib/store';
import axios from 'axios';

export default function Home() {
  const { userId, setIntegrations } = useStore();

  useEffect(() => {
    // Initial fetch of integration status
    const fetchStatus = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/auth/status/${userId}`);
        setIntegrations(res.data);
      } catch (e) {
        console.error("Could not fetch integrations", e);
      }
    };
    fetchStatus();
  }, [userId, setIntegrations]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="max-w-4xl mx-auto space-y-8">
          
          <header className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight mb-2">Good Morning, Developer</h1>
            <p className="text-gray-400">Here is your unified intelligence dashboard.</p>
          </header>

          <MorningBriefing />
          
          <UnifiedFeed />
          
        </div>
      </main>
    </div>
  );
}
