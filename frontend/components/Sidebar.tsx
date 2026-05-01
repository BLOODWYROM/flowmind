"use client";

import { useStore } from '../lib/store';
import { Mail, Activity, LogOut, CheckCircle } from 'lucide-react';
import axios from 'axios';

const GithubIcon = ({ size = 20, className = "" }: { size?: number, className?: string }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.24c3-.34 6-1.53 6-6.76 0-1.5-.5-2.8-1.4-3.8.1-.3.6-1.8-.1-3.7 0 0-1.2-.4-3.9 1.4a12.3 12.3 0 0 0-7 0C4.1 2 2.9 2.4 2.9 2.4c-.7 1.9-.2 3.4-.1 3.7A6.9 6.9 0 0 0 1.4 12c0 5.2 3 6.4 6 6.76-.7.6-1 1.5-1 2.9v4" />
    <path d="M4 20c-1.5 0-2.5-1-2.5-1" />
  </svg>
);

export default function Sidebar() {
  const { integrations, setIntegrations, userId } = useStore();

  const handleConnect = async (toolName: string) => {
    try {
      await axios.post('http://localhost:8000/api/auth/connect-tool', {
        user_id: userId,
        tool_name: toolName
      });
      // Refresh status
      const res = await axios.get(`http://localhost:8000/api/auth/status/${userId}`);
      setIntegrations(res.data);
    } catch (e) {
      console.error('Failed to connect tool', e);
    }
  };

  return (
    <div className="w-64 bg-[var(--color-card)] border-r border-[var(--color-border)] h-screen p-6 flex flex-col">
      <div className="flex items-center gap-3 mb-10 text-[var(--color-primary)]">
        <Activity size={28} />
        <h1 className="text-2xl font-bold tracking-tight">FlowMind</h1>
      </div>

      <div className="flex-1 space-y-6">
        <div>
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Integrations</h2>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-lg bg-[var(--color-background)] border border-[var(--color-border)]">
              <div className="flex items-center gap-3">
                <GithubIcon size={20} className="text-white" />
                <span className="font-medium text-sm">GitHub</span>
              </div>
              {integrations.github ? (
                <CheckCircle size={18} className="text-green-500" />
              ) : (
                <button 
                  onClick={() => handleConnect('github')}
                  className="text-xs bg-[var(--color-primary)] text-white px-3 py-1 rounded-full hover:opacity-90 transition"
                >
                  Connect
                </button>
              )}
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-[var(--color-background)] border border-[var(--color-border)]">
              <div className="flex items-center gap-3">
                <Mail size={20} className="text-red-400" />
                <span className="font-medium text-sm">Gmail</span>
              </div>
              {integrations.gmail ? (
                <CheckCircle size={18} className="text-green-500" />
              ) : (
                <button 
                  onClick={() => handleConnect('gmail')}
                  className="text-xs bg-[var(--color-primary)] text-white px-3 py-1 rounded-full hover:opacity-90 transition"
                >
                  Connect
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="pt-6 border-t border-[var(--color-border)]">
        <button className="flex items-center gap-3 text-gray-400 hover:text-white transition w-full p-2 rounded-md hover:bg-[var(--color-background)]">
          <LogOut size={18} />
          <span className="text-sm font-medium">Log out</span>
        </button>
      </div>
    </div>
  );
}
