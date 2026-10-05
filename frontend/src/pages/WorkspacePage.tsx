import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Activity, Database, Settings, ArrowRight, PanelLeft, PanelRight, ChevronDown, ChevronRight, MessageSquare, Plus, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Fuse from 'fuse.js';
import SettingsModal from '../components/SettingsModal';

interface ToolUI {
  id: string;
  name: string;
  category: string;
  icon: string;
  accentColor: string;
}

interface EventData {
  type: string;
  execution_id: string;
  tool_id?: string;
  duration_ms?: number;
  output?: any;
  input?: any;
  metadata?: any;
  error?: string;
}

interface MessageData {
  role: string;
  content: string;
  execution_id?: string;
}

export default function WorkspacePage() {
  const [tools, setTools] = useState<ToolUI[]>([]);
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [input, setInput] = useState('');
  const [events, setEvents] = useState<EventData[]>([]);
  const [isExecuting, setIsExecuting] = useState(false);
  
  const [leftOpen, setLeftOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  
  const [activeExecutionId, setActiveExecutionId] = useState<string | null>(null);
  const [expandedEvents, setExpandedEvents] = useState<Set<number>>(new Set());
  
  const [sessionId, setSessionId] = useState(() => {
    let id = localStorage.getItem('agentlab_session_id');
    if (!id) {
      id = "sess_" + Math.random().toString(36).substring(2, 9);
      localStorage.setItem('agentlab_session_id', id);
    }
    return id;
  });

  const handleNewSession = () => {
    const newId = "sess_" + Math.random().toString(36).substring(2, 9);
    localStorage.setItem('agentlab_session_id', newId);
    setSessionId(newId);
    setMessages([]);
    setEvents([]);
    setActiveExecutionId(null);
  };

  const handleClearChat = () => {
    setMessages([]);
    setEvents([]);
    setActiveExecutionId(null);
    localStorage.removeItem(`agentlab_history_${sessionId}`);
  };

  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  // Load tools
  useEffect(() => {
    fetch('http://localhost:8000/api/v1/tools')
      .then(res => res.json())
      .then(data => setTools(data))
      .catch(err => console.error("Failed to load tools", err));
  }, []);

  // Load chat history
  useEffect(() => {
    const history = localStorage.getItem(`agentlab_history_${sessionId}`);
    if (history) {
      try {
        setMessages(JSON.parse(history));
      } catch(e) {}
    }
  }, [sessionId]);

  // Save chat history
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(`agentlab_history_${sessionId}`, JSON.stringify(messages));
    }
  }, [messages, sessionId]);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    
    // RAG: Find relevant past messages using Fuse.js
    const fuse = new Fuse(messages, {
      keys: ['content'],
      threshold: 0.4,
      distance: 100
    });
    const ragResults = fuse.search(userMessage).map(res => res.item).slice(0, 5); // top 5
    // Maintain chronological order for injected context
    const contextMessages = messages.filter(m => ragResults.includes(m));

    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsExecuting(true);

    try {
      const provider = localStorage.getItem('agentlab_provider') || 'groq';
      const model = localStorage.getItem('agentlab_model') || 'openai/gpt-oss-120b';
      const apiKey = localStorage.getItem('agentlab_api_key') || '';

      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          session_id: sessionId, 
          message: userMessage,
          provider,
          model,
          api_key: apiKey,
          context_messages: contextMessages
        })
      });

      if (!response.body) return;
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      let finalContent = "";
      let currentExecutionId = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6);
            if (!dataStr) continue;
            try {
              const event: EventData = JSON.parse(dataStr);
              setEvents(prev => [...prev, event]);
              
              if (event.type === 'agent.started') {
                currentExecutionId = event.execution_id;
                setActiveExecutionId(currentExecutionId);
                setMessages(prev => {
                   const newArr = [...prev];
                   if (newArr.length > 0) {
                     newArr[newArr.length - 1].execution_id = currentExecutionId;
                   }
                   return newArr;
                });
              }
              
              if (event.type === 'agent.completed' && event.metadata?.content) {
                finalContent = event.metadata.content;
              }
            } catch (e) {
              console.error("Failed to parse event", e);
            }
          }
        }
      }
      
      if (finalContent && currentExecutionId) {
        setMessages(prev => [...prev, { role: 'assistant', content: finalContent, execution_id: currentExecutionId }]);
      }
    } catch (error) {
      console.error("Chat error", error);
    } finally {
      setIsExecuting(false);
    }
  };

  const toggleEvent = (idx: number) => {
    const next = new Set(expandedEvents);
    if (next.has(idx)) next.delete(idx);
    else next.add(idx);
    setExpandedEvents(next);
  };

  const visibleEvents = events.filter(e => e.execution_id === activeExecutionId);

  return (
    <div className="h-screen flex bg-canvas-base overflow-hidden">
      {showSettings && <SettingsModal onClose={() => setShowSettings(false)} />}
      
      {/* Navigation Rail / Left Column */}
      {leftOpen && (
        <aside className="w-[260px] border-r border-border-color bg-surface-primary flex flex-col hidden lg:flex">
          <div className="p-4 border-b border-border-color flex items-center gap-2">
            <Terminal className="text-accent-cyan" size={20} />
            <span className="font-display font-bold tracking-tight">AgentLab</span>
          </div>
          
          <div className="p-4 border-b border-border-color">
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-mono text-gray-500 uppercase tracking-widest">Sessions</span>
              <button onClick={handleNewSession} className="text-gray-400 hover:text-white transition-colors" title="New Session">
                <Plus size={16} />
              </button>
            </div>
            <div className="flex items-center gap-2 p-2 rounded bg-surface-secondary text-gray-300">
              <MessageSquare size={16} />
              <span className="font-sans text-sm truncate">Session {sessionId.substring(5)}</span>
            </div>
          </div>

          <div className="p-4 flex-1 overflow-y-auto">
            <div className="text-xs font-mono text-gray-500 uppercase tracking-widest mb-4">Available Tools</div>
            <div className="space-y-2">
              {tools.map(tool => (
                <div key={tool.id} className="flex items-center gap-3 p-2 rounded bg-surface-secondary border border-border-color">
                  <div 
                    className="w-2 h-2 rounded-full" 
                    style={{ backgroundColor: tool.accentColor }} 
                  />
                  <span className="font-mono text-sm truncate">{tool.name}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="p-4 border-t border-border-color">
            <div 
              onClick={() => setShowSettings(true)}
              className="flex items-center gap-3 text-gray-400 hover:text-white cursor-pointer transition-colors"
            >
              <Settings size={18} />
              <span className="font-sans text-sm">Settings</span>
            </div>
          </div>
        </aside>
      )}

      {/* Workspace / Center Column */}
      <main className="flex-1 flex flex-col bg-canvas-base relative">
        <header className="flex justify-between items-center p-3 border-b border-border-color bg-surface-primary">
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setLeftOpen(!leftOpen)}
              className="p-2 text-gray-400 hover:text-white rounded hover:bg-surface-elevated transition-colors"
            >
              <PanelLeft size={18} />
            </button>
          </div>
          
          <span className="font-mono text-xs uppercase tracking-widest text-gray-500">Agent Session</span>
          
          <div className="flex items-center gap-2">
            <button 
              onClick={handleClearChat}
              className="p-2 text-gray-400 hover:text-accent-red rounded hover:bg-surface-elevated transition-colors"
              title="Clear Chat"
            >
              <Trash2 size={16} />
            </button>
            <button 
              onClick={() => setRightOpen(!rightOpen)}
              className="p-2 text-gray-400 hover:text-white rounded hover:bg-surface-elevated transition-colors"
            >
              <PanelRight size={18} />
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-gray-500 font-mono text-sm space-y-2">
              <div>[ SYSTEM READY ] Awaiting input...</div>
            </div>
          )}
          
          {messages.map((msg, idx) => {
            const isActive = msg.execution_id && msg.execution_id === activeExecutionId;
            return (
              <div 
                key={idx} 
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} ${isActive ? 'opacity-100' : 'opacity-70'} transition-opacity cursor-pointer`}
                onClick={() => msg.execution_id && setActiveExecutionId(msg.execution_id)}
              >
                <div className={`max-w-[80%] min-w-[280px] p-4 rounded-lg border ${
                  msg.role === 'user' 
                    ? 'bg-surface-elevated border-border-elevated text-gray-200' 
                    : 'bg-surface-secondary border-border-color text-gray-300'
                } ${isActive ? 'ring-1 ring-accent-cyan ring-opacity-50' : ''}`}>
                  <div className="text-xs font-mono text-gray-500 mb-2 uppercase flex justify-between">
                    <span>{msg.role}</span>
                    {msg.execution_id && <span className="text-[10px] opacity-50">Click for telemetry</span>}
                  </div>
                  <div className="font-sans text-sm prose prose-invert prose-p:leading-relaxed prose-pre:bg-surface-primary prose-pre:border prose-pre:border-border-color max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            );
          })}
          <div ref={endOfMessagesRef} />
        </div>
        
        <div className="p-4 border-t border-border-color bg-surface-primary">
          <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto flex items-center">
            <input 
              type="text" 
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Command the agent..."
              disabled={isExecuting}
              className="w-full bg-surface-secondary border border-border-color rounded py-3 px-4 pl-4 pr-12 focus:outline-none focus:border-accent-cyan font-sans transition-colors disabled:opacity-50"
            />
            <button 
              type="submit" 
              disabled={isExecuting || !input.trim()}
              className="absolute right-2 p-2 text-gray-400 hover:text-accent-cyan transition-colors disabled:opacity-50"
            >
              <ArrowRight size={20} />
            </button>
          </form>
        </div>
      </main>

      {/* Activity & Telemetry / Right Column */}
      {rightOpen && (
        <aside className="w-[380px] border-l border-border-color bg-surface-primary hidden xl:flex flex-col">
          <div className="p-4 border-b border-border-color flex items-center gap-2">
            <Activity className="text-accent-cyan" size={18} />
            <span className="font-mono text-xs uppercase tracking-widest text-gray-400">
              Live Telemetry {visibleEvents.length > 0 && <span className="ml-2 px-2 py-0.5 bg-surface-secondary rounded">Focus</span>}
            </span>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {visibleEvents.length === 0 && (
              <div className="text-gray-500 font-mono text-xs text-center mt-10">
                No telemetry available for selected interaction.
              </div>
            )}
            
            {visibleEvents.map((ev, idx) => {
              const globalIdx = events.indexOf(ev);
              const isExpanded = expandedEvents.has(globalIdx);
              let color = '#6F7787'; // default
              if (ev.type === 'tool.started') color = '#22D3EE';
              if (ev.type === 'tool.completed') color = '#34D399';
              if (ev.type === 'tool.failed') color = '#F87171';
              
              const hasPayload = ev.input || ev.output;
              
              return (
                <div key={globalIdx} className="relative pl-4 border-l border-border-color border-opacity-50 pb-2">
                  <div 
                    className="absolute -left-[5px] top-1 w-[9px] h-[9px] rounded-full border-2 border-surface-primary"
                    style={{ backgroundColor: color }}
                  />
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-mono text-xs mb-1" style={{ color }}>{ev.type}</div>
                      {ev.tool_id && <div className="text-sm font-sans text-gray-300">Tool: {ev.tool_id}</div>}
                      {ev.duration_ms && <div className="text-xs font-mono text-gray-500">Latency: {ev.duration_ms}ms</div>}
                      {ev.error && <div className="text-xs font-mono text-accent-red mt-1 break-words">{ev.error}</div>}
                    </div>
                    
                    {hasPayload && (
                      <button 
                        onClick={() => toggleEvent(globalIdx)}
                        className="text-gray-500 hover:text-white transition-colors"
                      >
                        {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                      </button>
                    )}
                  </div>
                  
                  {isExpanded && hasPayload && (
                    <div className="mt-2 p-2 bg-surface-secondary border border-border-color rounded text-[10px] font-mono overflow-x-auto text-gray-300">
                      {ev.input && (
                        <div className="mb-2">
                          <span className="text-gray-500 mb-1 block">INPUT</span>
                          <pre className="m-0">{JSON.stringify(ev.input, null, 2)}</pre>
                        </div>
                      )}
                      {ev.output && (
                        <div>
                          <span className="text-gray-500 mb-1 block">OUTPUT</span>
                          <pre className="m-0">{JSON.stringify(ev.output, null, 2)}</pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </aside>
      )}
    </div>
  );
}
