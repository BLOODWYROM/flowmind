"use client";

import React from 'react';
import { signIn } from 'next-auth/react';
import { BrainCircuit, GitBranch, Mail } from 'lucide-react';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="w-full max-w-md z-10">
        <div className="glass-panel rounded-2xl p-8 shadow-2xl border border-white/5 backdrop-blur-xl">
          
          <div className="flex flex-col items-center text-center mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-[0_0_30px_rgba(99,102,241,0.5)] mb-6">
              <BrainCircuit size={32} className="text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white tracking-tight mb-2">Welcome to FlowMind</h1>
            <p className="text-zinc-400">Sign in to access your unified intelligence dashboard.</p>
          </div>

          <div className="flex flex-col gap-3">
            <button
              onClick={() => signIn('github', { callbackUrl: '/' })}
              className="w-full flex items-center justify-center gap-3 px-6 py-3.5 bg-white text-black hover:bg-zinc-200 transition-all font-semibold rounded-xl shadow-[0_0_15px_rgba(255,255,255,0.1)] group"
            >
              <GitBranch size={20} className="text-black group-hover:-translate-y-0.5 transition-transform" />
              <span>Continue with GitHub</span>
            </button>

            <button
              onClick={() => signIn('google', { callbackUrl: '/' })}
              className="w-full flex items-center justify-center gap-3 px-6 py-3.5 bg-zinc-900 text-white border border-white/10 hover:bg-zinc-800 transition-all font-semibold rounded-xl group"
            >
              <Mail size={20} className="text-white group-hover:-translate-y-0.5 transition-transform" />
              <span>Continue with Google</span>
            </button>
          </div>
          
          <div className="mt-6 text-center text-xs text-zinc-500">
            By continuing, you agree to allow FlowMind to securely sync and prioritize your developer notifications.
          </div>
        </div>
      </div>
    </div>
  );
}
