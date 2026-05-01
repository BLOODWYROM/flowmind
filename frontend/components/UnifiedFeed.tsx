"use client";

import { useStore, Item } from '../lib/store';
import { formatDistanceToNow } from 'date-fns';
import { Mail, AlertTriangle, Info, EyeOff, ExternalLink, CheckCircle2 } from 'lucide-react';

const GithubIcon = ({ size = 20, className = "" }: { size?: number, className?: string }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.24c3-.34 6-1.53 6-6.76 0-1.5-.5-2.8-1.4-3.8.1-.3.6-1.8-.1-3.7 0 0-1.2-.4-3.9 1.4a12.3 12.3 0 0 0-7 0C4.1 2 2.9 2.4 2.9 2.4c-.7 1.9-.2 3.4-.1 3.7A6.9 6.9 0 0 0 1.4 12c0 5.2 3 6.4 6 6.76-.7.6-1 1.5-1 2.9v4" />
    <path d="M4 20c-1.5 0-2.5-1-2.5-1" />
  </svg>
);

export default function UnifiedFeed() {
  const { items } = useStore();

  const getPriorityColors = (tag: string) => {
    switch(tag) {
      case 'Action Required':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      case 'FYI':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      case 'Ignore':
      default:
        return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
    }
  };

  const getPriorityIcon = (tag: string) => {
    switch(tag) {
      case 'Action Required': return <AlertTriangle size={14} />;
      case 'FYI': return <Info size={14} />;
      case 'Ignore': default: return <EyeOff size={14} />;
    }
  };

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500 border border-dashed border-[var(--color-border)] rounded-xl mt-8">
        <CheckCircle2 size={48} className="mb-4 opacity-50" />
        <p>No notifications. You're all caught up!</p>
      </div>
    );
  }

  return (
    <div className="mt-8 space-y-4">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Unified Inbox</h3>
      
      {items.map((item) => (
        <div key={item.id} className={`p-5 rounded-xl border bg-[var(--color-card)] flex flex-col gap-3 transition hover:border-gray-600 ${item.priority_tag === 'Action Required' ? 'border-red-900/50' : 'border-[var(--color-border)]'}`}>
          
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-md bg-[var(--color-background)]">
                {item.tool_name === 'github' ? <GithubIcon size={18} /> : <Mail size={18} className="text-red-400" />}
              </div>
              <div>
                <h4 className="font-medium text-white flex items-center gap-2">
                  {item.title}
                  <a href={item.url} target="_blank" rel="noreferrer" className="text-gray-500 hover:text-white">
                    <ExternalLink size={14} />
                  </a>
                </h4>
                <p className="text-xs text-gray-400">From {item.author} • {formatDistanceToNow(new Date(item.timestamp), {addSuffix: true})}</p>
              </div>
            </div>
            
            <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-xs font-medium ${getPriorityColors(item.priority_tag)}`}>
              {getPriorityIcon(item.priority_tag)}
              {item.priority_tag}
            </div>
          </div>

          <div className="text-sm text-gray-300 line-clamp-2 mt-1">
            {item.content}
          </div>

          {item.ai_explanation && (
            <div className="mt-2 bg-blue-900/20 border border-blue-800/30 p-3 rounded-lg flex items-start gap-3">
              <div className="mt-0.5 text-blue-400">✨</div>
              <p className="text-sm text-blue-200/80 leading-relaxed italic">
                {item.ai_explanation}
              </p>
            </div>
          )}
          
        </div>
      ))}
    </div>
  );
}
