# AgentLab

A production-quality AI Agent platform designed for real-time telemetry, modular extensibility, and developer-grade execution.

## 🏗 Architecture & "Extension-First" Principles

AgentLab follows a strict "Extension-First" architecture. The codebase is organized by domain and feature modules rather than giant buckets. This ensures you can add new tools, language models, or frontend pages without refactoring existing logic.

### 1. Tool Registry & Contract
- **Interface**: All tools inherit from `src.tools.interfaces.Tool`. Every tool must define its ID, schema, and `execute()` logic.
- **Registry**: The `ToolRegistry` dynamically holds available tools. Adding a new tool is simply a matter of registering it on startup. The LLM agent dynamically queries `registry.get_all_schemas()`—there are no hardcoded if/else tool checks.

### 2. LLM Provider & Agent Abstraction
- **Interfaces**: Agents depend on `LLMProvider` (e.g., `GroqProvider`), completely decoupling the LLM API logic from the business logic. Switching to OpenAI just requires implementing a new `OpenAIProvider`.
- **Event-Driven**: The agent's `execute()` method returns an AsyncGenerator yielding structured events (`agent.started`, `tool.started`, `tool.completed`). This allows the frontend to stream real-time telemetry natively.

### 3. Modular Frontend (React + Vite + Tailwind)
- **Generic Components**: The UI renders tools generically using the metadata provided by the backend (`/api/v1/tools`), meaning the frontend does not need a new component when a new tool is added.
- **Cinematic & Telemetric Design**: Follows the dark-mode, brutalist, and telemetric style definitions provided in the Stitch design system. 

## 📁 Folder Structure

### Backend (FastAPI - Python)
```text
backend/
├── src/
│   ├── core/           # Config, centralized errors, logging
│   ├── agent/          # Agent logic, events, messages, LLM providers
│   ├── tools/          # Tool interfaces, registry, specific tool implementations
│   ├── api/            # FastAPI routes and schemas
│   └── infrastructure/ # DB/Repository abstractions (ready for integration)
├── main.py             # App entry point
└── requirements.txt    # Python dependencies
```

### Frontend (React/Vite - TypeScript)
```text
frontend/
├── src/
│   ├── components/     # Generic modular UI components
│   ├── pages/          # LandingPage, WorkspacePage
│   ├── App.tsx         # React Router setup
│   └── index.css       # Tailwind & Font configs
├── tailwind.config.js  # Strict design system color/spacing configuration
└── package.json
```

## 🚀 Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```
**Environment Variables**:
Create a `.env` file in `backend/` and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Run the Backend**:
```bash
python -m src.main
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The React App will run at `http://localhost:5173`.

## 🛠 Adding a New Tool

1. Create `src/tools/my_tool.py`.
2. Inherit from `Tool` and define `id`, `input_schema`, `ui_config`, and `execute()`.
3. In `main.py`, simply add `registry.register(MyNewTool())`.
4. The Agent will instantly have access to it, and the Frontend will instantly render its icon in the UI. No other changes are needed!
