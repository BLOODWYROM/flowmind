'use client';

import React, { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useFeedStore } from '../store';
import { Sidebar } from '../components/Sidebar';
import { ItemCard } from '../components/ItemCard';
import { BriefingPanel } from '../components/BriefingPanel';
import { Loader2, RefreshCw, Layers } from 'lucide-react';

export default function Home() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { items, briefing, loading, fetchItems, fetchBriefing, triggerPipeline } = useFeedStore();
  
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
    }
  }, [status, router]);

  // @ts-ignore
  const userId = (session?.user as any)?.id || 1;

  useEffect(() => {
    if (status === 'authenticated') {
      fetchItems(userId);
      fetchBriefing(userId);
    }
  }, [status, userId, fetchItems, fetchBriefing]);

  const handleTrigger = () => {
    triggerPipeline(userId);
  };

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 size={32} className="animate-spin text-zinc-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex font-sans selection:bg-purple-500/30">
      <Sidebar />
      
      <main className="flex-1 ml-64 p-8">
        <div className="max-w-4xl mx-auto">
          <header className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold tracking-tight mb-1 text-white">Unified Intelligence</h1>
              <p className="text-muted-foreground text-sm">Your AI-curated developer notifications</p>
            </div>
            
            <button 
              onClick={handleTrigger}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2.5 bg-white text-black font-semibold rounded-lg hover:bg-zinc-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(255,255,255,0.1)]"
            >
              {loading ? <Loader2 size={18} className="animate-spin" /> : <RefreshCw size={18} />}
              <span>{loading ? 'Processing...' : 'Run Pipeline'}</span>
            </button>
          </header>

          {loading && items.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
              <Loader2 size={40} className="animate-spin mb-4 text-zinc-500" />
              <p>Analyzing notifications with Gemini...</p>
            </div>
          )}

          {!loading && <BriefingPanel briefing={briefing} />}

          {!loading && items.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-4 px-1">
                <Layers size={18} className="text-zinc-400" />
                <h2 className="text-lg font-semibold text-zinc-200 tracking-tight">Priority Queue</h2>
              </div>
              
              <div className="space-y-4">
                {items.map(item => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            </div>
          )}

          {!loading && items.length === 0 && (
            <div className="glass-panel rounded-xl p-12 text-center flex flex-col items-center">
              <div className="w-16 h-16 rounded-full bg-zinc-800/50 flex items-center justify-center mb-4">
                <Layers size={24} className="text-zinc-500" />
              </div>
              <h3 className="text-xl font-medium text-white mb-2">No Notifications</h3>
              <p className="text-muted-foreground max-w-sm">
                Your queue is empty. Run the pipeline to fetch and prioritize your latest GitHub and Gmail updates.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
