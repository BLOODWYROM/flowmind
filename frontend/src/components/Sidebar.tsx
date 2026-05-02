'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { 
  LayoutDashboard, 
  Settings, 
  GitBranch, 
  Mail, 
  BrainCircuit,
  LogOut 
} from 'lucide-react';
import { signOut } from 'next-auth/react';
import Link from 'next/link';
import { useFeedStore } from '../store';

export function Sidebar() {
  const pathname = usePathname();
  const { data: session, status } = useSession();
  const user = session?.user;
  const { integrationStatus, fetchIntegrationStatus } = useFeedStore();

  // @ts-ignore
  const userId = (session?.user as any)?.id || 1;

  useEffect(() => {
    if (status === 'authenticated') {
      fetchIntegrationStatus(userId);
    }
  }, [status, userId, fetchIntegrationStatus]);

  return (
    <aside className="w-64 h-screen glass-panel fixed left-0 top-0 border-r border-border flex flex-col p-4 z-10">
      <div className="flex items-center gap-3 mb-10 mt-2 px-2">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
          <BrainCircuit size={20} className="text-white" />
        </div>
        <h1 className="font-bold text-xl tracking-tight text-white">FlowMind</h1>
      </div>
      
      <div className="space-y-6 flex-1">
        <div>
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2">Main</p>
          <nav className="space-y-1">
            <Link 
              href="/" 
              className={`flex items-center gap-3 px-3 py-2.5 rounded-md font-medium transition-colors ${
                pathname === '/' ? 'bg-secondary text-white' : 'text-muted-foreground hover:bg-secondary/50 hover:text-white'
              }`}
            >
              <LayoutDashboard size={18} />
              <span>Dashboard</span>
            </Link>
          </nav>
        </div>
        
        <div>
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2">Integrations</p>
          <nav className="space-y-1">
            <a 
              href="https://github.com/settings/applications" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center justify-between px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <GitBranch size={18} />
                <span>GitHub</span>
              </div>
              <div className={`w-2 h-2 rounded-full ${integrationStatus.github ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]' : 'bg-zinc-600'}`}></div>
            </a>
            <a 
              href="https://mail.google.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center justify-between px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <Mail size={18} />
                <span>Gmail</span>
              </div>
              <div className={`w-2 h-2 rounded-full ${integrationStatus.gmail ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]' : 'bg-zinc-600'}`}></div>
            </a>
          </nav>
        </div>
      </div>

      {/* User Profile */}
      {user && (
        <div className="mb-3 px-2 py-3 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
          <div className="flex items-center gap-3">
            {user.image ? (
              <img src={user.image} alt="" className="w-8 h-8 rounded-full" />
            ) : (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-sm font-bold">
                {user.name?.charAt(0) || '?'}
              </div>
            )}
            <div className="truncate">
              <p className="text-sm text-white font-medium truncate">{user.name || 'Developer'}</p>
              <p className="text-xs text-zinc-500 truncate">{user.email || ''}</p>
            </div>
          </div>
        </div>
      )}
      
      <div className="pt-4 border-t border-border">
        <nav className="space-y-1">
          <Link 
            href="/settings" 
            className={`flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors ${
              pathname === '/settings' ? 'bg-secondary text-white' : 'text-muted-foreground hover:bg-secondary/50 hover:text-white'
            }`}
          >
            <Settings size={18} />
            <span>Settings</span>
          </Link>
          <button 
            onClick={() => signOut({ callbackUrl: '/login' })}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-red-500/10 text-muted-foreground hover:text-red-400 transition-colors"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </nav>
      </div>
    </aside>
  );
}
