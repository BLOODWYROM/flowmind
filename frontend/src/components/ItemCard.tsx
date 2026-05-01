import React from 'react';
import { Github, Mail, AlertTriangle, Info, BellOff, ExternalLink } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { FeedItem } from '../store';

export function ItemCard({ item }: { item: FeedItem }) {
  const isGithub = item.tool_name === 'github';
  
  const getTagStyle = (tag: string) => {
    switch (tag) {
      case 'Action Required':
        return 'tag-action';
      case 'FYI':
        return 'tag-fyi';
      case 'Ignore':
        return 'tag-ignore';
      default:
        return 'bg-zinc-800 text-zinc-300';
    }
  };

  const getTagIcon = (tag: string) => {
    switch (tag) {
      case 'Action Required':
        return <AlertTriangle size={14} className="mr-1" />;
      case 'FYI':
        return <Info size={14} className="mr-1" />;
      case 'Ignore':
        return <BellOff size={14} className="mr-1" />;
      default:
        return null;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'score-high';
    if (score >= 5) return 'score-medium';
    return 'score-low';
  };

  return (
    <div className="glass-panel rounded-xl p-5 hover:bg-zinc-800/80 transition-all group">
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${isGithub ? 'bg-zinc-800 text-white' : 'bg-red-500/10 text-red-500'}`}>
            {isGithub ? <Github size={18} /> : <Mail size={18} />}
          </div>
          <div>
            <h3 className="font-semibold text-lg text-white group-hover:text-blue-400 transition-colors flex items-center gap-2">
              {item.title}
              <ExternalLink size={14} className="opacity-0 group-hover:opacity-100 transition-opacity text-blue-400 cursor-pointer" />
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
      
      <div className="flex items-center gap-3 pt-3 border-t border-border">
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
