import React, { useState, useEffect } from 'react';

interface SettingsModalProps {
  onClose: () => void;
}

export default function SettingsModal({ onClose }: SettingsModalProps) {
  const [provider, setProvider] = useState(() => localStorage.getItem('agentlab_provider') || 'groq');
  const [model, setModel] = useState(() => localStorage.getItem('agentlab_model') || 'openai/gpt-oss-120b');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('agentlab_api_key') || '');

  const handleSave = () => {
    localStorage.setItem('agentlab_provider', provider);
    localStorage.setItem('agentlab_model', model);
    localStorage.setItem('agentlab_api_key', apiKey);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-surface-primary border border-border-color rounded-lg w-full max-w-md p-6">
        <h2 className="font-display font-bold text-xl mb-4 text-white">Platform Settings</h2>
        
        <div className="space-y-4 font-sans text-sm">
          <div>
            <label className="block text-gray-400 mb-1">Provider</label>
            <select 
              value={provider}
              onChange={e => setProvider(e.target.value)}
              className="w-full bg-surface-secondary border border-border-color rounded p-2 text-white focus:outline-none focus:border-accent-cyan"
            >
              <option value="groq">Groq</option>
              <option value="openai">OpenAI (or Compatible)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-gray-400 mb-1">Model Name</label>
            <input 
              type="text" 
              value={model}
              onChange={e => setModel(e.target.value)}
              className="w-full bg-surface-secondary border border-border-color rounded p-2 text-white focus:outline-none focus:border-accent-cyan"
              placeholder="e.g. gpt-4o, llama-3.3-70b-versatile"
            />
          </div>
          
          <div>
            <label className="block text-gray-400 mb-1">API Key</label>
            <input 
              type="password" 
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              className="w-full bg-surface-secondary border border-border-color rounded p-2 text-white focus:outline-none focus:border-accent-cyan"
              placeholder="Enter your personal API key"
            />
            <p className="text-[10px] text-gray-500 mt-1">
              Your key is stored strictly in your browser's LocalStorage and sent only to your local backend.
            </p>
          </div>
        </div>
        
        <div className="mt-6 flex justify-end gap-2">
          <button 
            onClick={onClose}
            className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button 
            onClick={handleSave}
            className="px-4 py-2 bg-gray-200 text-canvas-base hover:bg-white rounded font-medium transition-colors"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}
