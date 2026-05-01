import React from 'react';
import { 
  LayoutDashboard, 
  Settings, 
  GitBranch, 
  Mail, 
  BrainCircuit,
  LogOut 
} from 'lucide-react';

import { signOut } from 'next-auth/react';

export function Sidebar() {
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
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-md bg-secondary text-white font-medium transition-colors">
              <LayoutDashboard size={18} />
              <span>Dashboard</span>
            </a>
          </nav>
        </div>
        
        <div>
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2">Integrations</p>
          <nav className="space-y-1">
            <div className="flex items-center justify-between px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                <GitBranch size={18} />
                <span>GitHub</span>
              </div>
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
            </div>
            <div className="flex items-center justify-between px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                <Mail size={18} />
                <span>Gmail</span>
              </div>
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
            </div>
          </nav>
        </div>
      </div>
      
      <div className="mt-auto pt-4 border-t border-border">
        <nav className="space-y-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors">
            <Settings size={18} />
            <span>Settings</span>
          </a>
          <button 
            onClick={() => signOut()}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-white transition-colors"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </nav>
      </div>
    </aside>
  );
}
