import React from 'react';
import { Sparkles } from 'lucide-react';

export function BriefingPanel({ briefing }: { briefing: string }) {
  if (!briefing) return null;

  return (
    <div className="relative overflow-hidden rounded-2xl glass-panel p-1 mb-8 group">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-indigo-500/10 opacity-50 transition-opacity group-hover:opacity-100"></div>
      <div className="relative bg-zinc-900/80 backdrop-blur-xl rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-lg">
            <Sparkles size={18} className="text-white" />
          </div>
          <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            AI Morning Briefing
          </h2>
        </div>
        
        <div className="prose prose-invert max-w-none">
          {briefing.split('\n').map((paragraph, idx) => (
            <p key={idx} className="text-zinc-300 leading-relaxed text-[15px] mb-3 last:mb-0">
              {paragraph}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}
