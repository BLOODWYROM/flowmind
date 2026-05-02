'use client';

import React, { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useFeedStore } from '../store';
import { Sidebar } from '../components/Sidebar';
import { ItemCard } from '../components/ItemCard';
import { BriefingPanel } from '../components/BriefingPanel';
import { Loader2, RefreshCw, Layers, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Home() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { items, briefing, loading, error, pipelineStatus, fetchItems, fetchBriefing, triggerPipeline } = useFeedStore();
  const [showAll, setShowAll] = React.useState(false);
  
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

  const getButtonLabel = () => {
    switch (pipelineStatus) {
      case 'running': return 'Analyzing...';
      case 'success': return 'Done!';
      case 'error': return 'Failed';
      default: return 'Run Pipeline';
    }
  };

  const getButtonIcon = () => {
    switch (pipelineStatus) {
      case 'running': return <Loader2 size={18} className="animate-spin" />;
      case 'success': return <CheckCircle2 size={18} />;
      case 'error': return <AlertCircle size={18} />;
      default: return <RefreshCw size={18} />;
    }
  };

  const getButtonStyle = () => {
    switch (pipelineStatus) {
      case 'success': return 'bg-green-500 text-white hover:bg-green-600';
      case 'error': return 'bg-red-500 text-white hover:bg-red-600';
      default: return 'bg-white text-black hover:bg-zinc-200';
    }
  };

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
              className={`flex items-center gap-2 px-5 py-2.5 font-semibold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(255,255,255,0.1)] ${getButtonStyle()}`}
            >
              {getButtonIcon()}
              <span>{getButtonLabel()}</span>
            </button>
          </header>

          {/* Error Toast */}
          {error && (
            <div className="mb-6 flex items-center gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-in fade-in">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          {/* Loading state during first pipeline run */}
          {loading && items.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
              <div className="relative mb-6">
                <div className="w-16 h-16 rounded-full border-2 border-zinc-800 flex items-center justify-center">
                  <Loader2 size={28} className="animate-spin text-purple-500" />
                </div>
                <div className="absolute inset-0 rounded-full bg-purple-500/10 animate-pulse"></div>
              </div>
              <p className="text-zinc-300 font-medium mb-1">Analyzing your notifications with Gemini AI...</p>
              <p className="text-zinc-500 text-sm">This may take up to 30 seconds</p>
            </div>
          )}

          {!loading && <BriefingPanel briefing={briefing} />}

          {!loading && items.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-4 px-1">
                <div className="flex items-center gap-2">
                  <Layers size={18} className="text-zinc-400" />
                  <h2 className="text-lg font-semibold text-zinc-200 tracking-tight">Priority Queue</h2>
                </div>
                <button 
                  onClick={() => setShowAll(!showAll)}
                  className="text-xs font-medium text-zinc-500 hover:text-zinc-300 transition-colors flex items-center gap-1.5 px-2 py-1 rounded-md hover:bg-zinc-800"
                >
                  {showAll ? "Hide low priority" : "Show all notifications"}
                  <span className="bg-zinc-800 px-1.5 py-0.5 rounded text-[10px]">
                    {items.length}
                  </span>
                </button>
              </div>
              
              <div className="space-y-4">
                {items
                  .filter(item => showAll || item.priority_tag !== 'Can Ignore')
                  .map(item => (
                    <ItemCard key={item.id} item={item} />
                  ))
                }
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
