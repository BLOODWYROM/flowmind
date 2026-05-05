'use client';

import React, { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { Sidebar } from '../../components/Sidebar';
import { useFeedStore } from '../../store';
import { 
  User, 
  Mail, 
  GitBranch, 
  Shield, 
  ExternalLink,
  CheckCircle2,
  XCircle,
  Loader2,
  MessageSquare
} from 'lucide-react';

export default function SettingsPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { integrationStatus, fetchIntegrationStatus } = useFeedStore();

  // @ts-ignore
  const userId = (session?.user as any)?.id || 1;

  useEffect(() => {
    if (status === 'authenticated') {
      fetchIntegrationStatus(userId);
    }
  }, [status, userId, fetchIntegrationStatus]);

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 size={32} className="animate-spin text-zinc-500" />
      </div>
    );
  }

  if (status === 'unauthenticated') {
    router.push('/login');
    return null;
  }

  const user = session?.user;

  return (
    <div className="min-h-screen bg-background text-foreground flex font-sans selection:bg-purple-500/30">
      <Sidebar />
      
      <main className="flex-1 ml-64 p-8">
        <div className="max-w-3xl mx-auto">
          <header className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight mb-1 text-white">Settings</h1>
            <p className="text-muted-foreground text-sm">Manage your account and integrations</p>
          </header>

          {/* Profile Section */}
          <div className="glass-panel rounded-xl p-6 mb-6">
            <div className="flex items-center gap-2 mb-5">
              <User size={18} className="text-zinc-400" />
              <h2 className="text-lg font-semibold text-zinc-200">Profile</h2>
            </div>
            
            <div className="flex items-center gap-4">
              {user?.image ? (
                <img src={user.image} alt="Avatar" className="w-16 h-16 rounded-full border-2 border-zinc-700 shadow-xl" />
              ) : (
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xl font-bold shadow-xl">
                  {user?.name?.charAt(0) || '?'}
                </div>
              )}
              <div>
                <p className="text-white text-lg font-semibold">{user?.name || 'Developer'}</p>
                <p className="text-zinc-400 text-sm">{user?.email || 'No email'}</p>
              </div>
            </div>
          </div>

          {/* Connected Accounts Section */}
          <div className="glass-panel rounded-xl p-6 mb-6">
            <div className="flex items-center gap-2 mb-5">
              <Shield size={18} className="text-zinc-400" />
              <h2 className="text-lg font-semibold text-zinc-200">Connected Accounts</h2>
            </div>
            
            <div className="space-y-4">
              {/* Google Account */}
              <div className="flex items-center justify-between p-4 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-red-500/10">
                    <Mail size={18} className="text-red-400" />
                  </div>
                  <div>
                    <p className="text-white font-medium">Google / Gmail</p>
                    <p className="text-zinc-500 text-xs">Read and analyze your inbox</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  {integrationStatus.gmail ? (
                    <>
                      <CheckCircle2 size={16} className="text-green-500" />
                      <span className="text-green-400 font-medium">Connected</span>
                    </>
                  ) : (
                    <>
                      <XCircle size={16} className="text-zinc-500" />
                      <span className="text-zinc-400 font-medium">Not Connected</span>
                    </>
                  )}
                </div>
              </div>

              {/* GitHub Account */}
              <div className="flex items-center justify-between p-4 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-zinc-800">
                    <GitBranch size={18} className="text-white" />
                  </div>
                  <div>
                    <p className="text-white font-medium">GitHub</p>
                    <p className="text-zinc-500 text-xs">Notifications, PRs, and issues</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  {integrationStatus.github ? (
                    <>
                      <CheckCircle2 size={16} className="text-green-500" />
                      <span className="text-green-400 font-medium">Connected</span>
                    </>
                  ) : (
                    <>
                      <XCircle size={16} className="text-zinc-500" />
                      <span className="text-zinc-400 font-medium">Not Connected</span>
                    </>
                  )}
                </div>
              </div>

              {/* Slack Account */}
              <div className="flex items-center justify-between p-4 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-[#4A154B]/20">
                    <MessageSquare size={18} className="text-[#E01E5A]" />
                  </div>
                  <div>
                    <p className="text-white font-medium">Slack</p>
                    <p className="text-zinc-500 text-xs">Unread messages and mentions</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  {integrationStatus.slack ? (
                    <>
                      <CheckCircle2 size={16} className="text-green-500" />
                      <span className="text-green-400 font-medium">Connected</span>
                    </>
                  ) : (
                    <>
                      <XCircle size={16} className="text-zinc-500" />
                      <span className="text-zinc-400 font-medium">Not Connected</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* About Section */}
          <div className="glass-panel rounded-xl p-6">
            <div className="flex items-center gap-2 mb-5">
              <ExternalLink size={18} className="text-zinc-400" />
              <h2 className="text-lg font-semibold text-zinc-200">About FlowMind</h2>
            </div>
            <p className="text-zinc-400 text-sm leading-relaxed mb-3">
              FlowMind is an AI-powered developer dashboard that uses Gemini to intelligently prioritize 
              your GitHub notifications and Gmail messages. It helps you focus on what matters most.
            </p>
            <div className="flex items-center gap-4 text-xs text-zinc-500">
              <span>Version 1.0.0</span>
              <span>•</span>
              <a href="https://github.com/BLOODWYROM/flowmind" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors">
                GitHub Repository
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
