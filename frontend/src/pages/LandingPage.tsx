import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal, Database, Activity } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col bg-canvas-base text-gray-200">
      <header className="px-8 py-6 flex justify-between items-center border-b border-border-color bg-surface-primary">
        <div className="flex items-center gap-2">
          <Terminal className="text-accent-cyan" size={24} />
          <span className="font-display font-bold text-xl tracking-tight">AgentLab</span>
        </div>
        <button 
          onClick={() => navigate('/workspace')}
          className="bg-gray-100 hover:bg-white text-canvas-base px-5 py-2 rounded font-medium transition-colors"
        >
          Launch Workspace
        </button>
      </header>
      
      <main className="flex-1 flex flex-col items-center justify-center p-8 max-w-5xl mx-auto text-center">
        <h1 className="font-display font-extrabold text-5xl md:text-7xl mb-6 leading-tight">
          Surgical precision. <br/>
          <span className="text-accent-cyan">Autonomous execution.</span>
        </h1>
        <p className="font-sans text-lg md:text-xl text-gray-400 max-w-2xl mb-12">
          A brutalist, high-density AI agent platform designed for developer-grade workflows and real-time telemetry.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-8">
          <div className="bg-surface-secondary border border-border-color p-6 rounded-lg text-left">
            <Terminal className="text-accent-cyan mb-4" size={28} />
            <h3 className="font-display font-bold text-lg mb-2">Extension-First</h3>
            <p className="text-sm text-gray-400">Zero-rewrite architecture for adding new tools and providers.</p>
          </div>
          <div className="bg-surface-secondary border border-border-color p-6 rounded-lg text-left">
            <Activity className="text-accent-purple mb-4" size={28} />
            <h3 className="font-display font-bold text-lg mb-2">Event-Driven</h3>
            <p className="text-sm text-gray-400">Real-time telemetry and structured execution traces.</p>
          </div>
          <div className="bg-surface-secondary border border-border-color p-6 rounded-lg text-left">
            <Database className="text-accent-green mb-4" size={28} />
            <h3 className="font-display font-bold text-lg mb-2">Abstracted Core</h3>
            <p className="text-sm text-gray-400">Database and provider interfaces decoupled from business logic.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
