import React from 'react';
import { GitBranch, Mail, AlertTriangle, Info, BellOff, ExternalLink, CheckCircle2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { FeedItem } from '../store';

export function ItemCard({ item }: { item: FeedItem }) {
  const isGithub = item.tool_name === 'github';
  
  const getTagStyle = (tag: string) => {
    switch (tag) {
      case 'Action Required':
        return 'bg-red-500/20 text-red-400 border border-red-500/30';
      case 'FYI':
        return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30';
      case 'Can Ignore':
        return 'bg-green-500/20 text-green-400 border border-green-500/30';
      default:
        return 'bg-zinc-800 text-zinc-300';
    }
  };

  const getTagIcon = (tag: string) => {
    switch (tag) {
      case 'Action Required':
        return <AlertTriangle size={14} className="mr-1.5" />;
      case 'FYI':
        return <Info size={14} className="mr-1.5" />;
      case 'Can Ignore':
        return <CheckCircle2 size={14} className="mr-1.5" />;
      default:
        return null;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'score-high';
    if (score >= 5) return 'score-medium';
    return 'score-low';
  };

  const handleClick = () => {
    window.open(item.url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div 
      onClick={handleClick}
      className="glass-panel rounded-xl p-5 hover:bg-zinc-800/80 transition-all group cursor-pointer border border-transparent hover:border-zinc-700/50"
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${isGithub ? 'bg-zinc-800 text-white' : 'bg-red-500/10 text-red-500'}`}>
            {isGithub ? <GitBranch size={18} /> : <Mail size={18} />}
          </div>
          <div>
            <h3 className="font-semibold text-lg text-white group-hover:text-blue-400 transition-colors flex items-center gap-2">
              {item.title}
              <ExternalLink size={14} className="opacity-0 group-hover:opacity-100 transition-opacity text-blue-400" />
            </h3>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span className="font-medium text-zinc-300">{item.author}</span>
              <span>•</span>
              <span>{formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="text-right">
            <span className={`text-xs font-bold px-2 py-1 rounded-md ${getScoreColor(item.priority_score)} bg-black/40`}>
              Score: {item.priority_score}/10
            </span>
          </div>
        </div>
      </div>
      
      <p className="text-zinc-300 text-sm mb-4 line-clamp-2 leading-relaxed">
        {item.content}
      </p>
      
      <div className="flex items-center gap-3 pt-3 border-t border-zinc-800/50">
        <span className={`flex items-center text-xs font-medium px-2.5 py-1 rounded-full ${getTagStyle(item.priority_tag)}`}>
          {getTagIcon(item.priority_tag)}
          {item.priority_tag}
        </span>
        <p className="text-xs text-muted-foreground italic truncate flex-1">
          <span className="text-blue-400/80 not-italic mr-1">AI Note:</span>
          {item.ai_explanation}
        </p>
      </div>
    </div>
  );
}
