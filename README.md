# 🤖 AGENT MINI

<p align="center">
  <strong>An Elite, Autonomous, Tool-Augmented AI Agent Operating in Your Terminal</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Architecture-Autonomous%20Agentic%20Loop-orange" alt="Architecture" />
  <img src="https://img.shields.io/badge/Providers-Groq%20%7C%20NVIDIA%20NIM%20%7C%20Custom-green" alt="Providers" />
  <img src="https://img.shields.io/badge/UI-Rich%20%2B%20Prompt%20Toolkit-purple" alt="UI" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License" />
</p>

---

## 🌟 Overview

**Agent MINI** is an intelligent, tool-augmented CLI software engineer and desktop assistant. Built with an autonomous reasoning loop, self-healing reflection, strict sandbox workspace isolation, and Human-in-the-Loop safety guardrails, Agent MINI can research the web, scaffold complete multi-file codebases, execute terminal tasks, inspect files, and interact with the local operating system—all through an interactive, responsive terminal UI.

---

## ✨ Key Features

### 🧠 1. Multi-Provider & Dynamic Model Switching
- **Provider Support**: Seamless integration with **Groq** (ultra-fast inference), **NVIDIA NIM**, and **Custom OpenAI-compatible gateways** (Omniroute, 9Router, Local LLMs).
- **Runtime Model Switching**: List all models live with `/models` and switch instantly using index numbers or model IDs (`/model 2` or `/model llama-3.3-70b-versatile`).
- **Reasoning Effort Control**: Fine-tune thinking depth for reasoning models on the fly with `/effort low`, `/effort medium`, or `/effort high`.

### 🛡️ 2. Human-in-the-Loop Safety Guardrails
- Automatically intercepts sensitive operations before execution:
  - Terminal command execution
  - Python code execution
  - File creation and file appending
  - Directory creation
  - External application launching
  - PDF document creation
- Interactive approval prompt with parameter breakdown:
  - `[y]` Allow action once
  - `[n]` Block action and return error feedback to the agent
  - `[always]` Trust all subsequent actions for the current session
- Toggle guardrails anytime using `/guard on` or `/guard off`.

### 🔄 3. Autonomous Self-Correction & Healing
- When a tool fails (missing directory, syntax error, path error), Agent MINI does not crash or give up.
- The built-in reflection harness detects the failure and prompts the model with an **Autonomous Healing Directive**, allowing it to self-diagnose, re-plan, and resolve the issue automatically.

### 💾 4. Session Persistence & Chat Management
- **Auto-Save**: Automatically persists chat history into `.sessions/` on exit (`/bye`).
- **Session Resume**: List previous sessions with `/sessions` and resume past conversations with `/load <num>`.
- **Markdown Export**: Export conversations into formatted GitHub-flavored markdown documents with `/export`.

### 📦 5. Sandbox Workspace Isolation & Root Protection
- **Safe Development**: All scaffolded projects, scripts, and web designs are isolated within `sandbox/<project_name>/`.
- **Root Protection**: Programmatic guard prevents the agent from polluting or accidentally overwriting files in the repository root.

### 📚 6. Skill-Based Extensibility
Agent MINI automatically loads modular markdown workflows from `Agent/skills/` before executing complex workflows:
- **`coding_helper`**: Enforces sequential, production-ready, multi-file code generation (HTML/CSS/JS/Python) without timeouts.
- **`web_research`**: Deep web search synthesis and source aggregation.
- **`file_operations`**: Safe inspection, reading, and editing of filesystem assets.
- **`system_admin`**: Safe diagnosis and execution of terminal utilities.

---

## 🛠️ Built-in Tools (14 Tools)

| Tool Name | Description |
|---|---|
| `web_search` | Real-time internet search via DuckDuckGo (`ddgs`) |
| `scrape_webpage` | Extracts and parses clean textual content from any HTTP/HTTPS URL |
| `read_file` | Reads contents of local files |
| `write_file` | Creates or writes complete files (with mandatory sandbox path enforcement) |
| `append_file` | Appends patches or sections incrementally to existing files |
| `list_files` | Inspects directory contents |
| `create_folder` | Creates directories recursively |
| `run_python_code` | Executes Python code in a sandboxed subprocess with timeout safeguards |
| `run_terminal_cammand` | Runs Windows shell / CLI commands (`ping`, `ipconfig`, `git`, etc.) |
| `find_application` | Locates installed desktop applications and shortcuts by name |
| `launch_app_by_path` | Launches desktop applications via executable or shortcut path |
| `read_skill` | Reads specialized skill guidelines before starting complex tasks |
| `create_pdf` | Generates formatted, clean PDF documents with custom titles and Markdown formatting |
| `get_current_time` | Fetches real-time system clock and date |

---

## ⚡ Slash Commands Reference

Type `/` in the CLI to see interactive autocomplete suggestions powered by `prompt_toolkit`:

| Command | Action | Example |
|---|---|---|
| `/models` | Displays all available models for active provider in a clean table | `/models` |
| `/model <name\|num>` | Switches active model permanently | `/model 3` or `/model llama-3.3-70b-versatile` |
| `/provider <name>` | Switches API provider (`groq`, `nvidia`, `custom`) | `/provider groq` |
| `/effort <level>` | Sets reasoning effort (`low`, `medium`, `high`) | `/effort medium` |
| `/guard <on\|off>` | Enables or disables interactive safety guardrails | `/guard on` |
| `/sessions` | Lists all previously saved conversation sessions | `/sessions` |
| `/load <num>` | Restores and resumes a previous session | `/load 1` |
| `/export` | Exports active chat session as a Markdown file | `/export` |
| `/color <name>` | Customizes terminal theme accent color | `/color cyan` |
| `/clear` | Clears current conversation memory | `/clear` |
| `/help` | Displays the command guide panel | `/help` |
| `/bye` / `/exit` | Auto-saves session and cleanly exits | `/bye` |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.12+**
- An API Key from any supported provider:
  - [Groq Console](https://console.groq.com/keys) *(Recommended for fastest inference)*
  - [NVIDIA NIM](https://build.nvidia.com/settings/api-keys)
  - Any OpenAI-compatible Gateway / Local endpoint

---

### 2. Installation

#### Option A: Automated Setup (Windows)
1. Clone the repository:
   ```powershell
   git clone https://github.com/Vishal-aiuser/Agent-MINI.git
   cd Agent-MINI
   ```
2. Double-click `setup.bat` (or run in terminal):
   ```powershell
   .\setup.bat
   ```

#### Option B: Manual Setup (`uv` or `pip`)
```powershell
# Using uv (Recommended for speed):
uv sync

# OR using standard pip:
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Environment Configuration

Copy the example environment file:
```powershell
copy .env.example .env
```

Open `.env` and configure your API key(s):
```env
# Groq API Config (Recommended for ultra-fast generation)
GROQ_BASE_URL="https://api.groq.com/openai/v1"
GROQ_API_KEY="your_groq_api_key_here"

# NVIDIA NIM API Config
NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY="your_nvidia_nim_api_key_here"

# Custom Gateway / Local LLM (e.g. Ollama, LM Studio, Omniroute)
CUSTOM_PROVIDER_BASE_URL="http://localhost:11434/v1"
CUSTOM_PROVIDER_API_KEY="your_custom_api_key"
```

You can also customize default preferences in `Agent/setup.json`:
```json
{
    "provider": "groq",
    "model": "llama-3.3-70b-versatile",
    "reasoning_effort": "medium",
    "box_color": "dark_orange",
    "box_style": "ASCII"
}
```

---

### 4. Running the Agent

Start the agent CLI:
```powershell
.\mini
```
*(Or double-click `mini.bat` in File Explorer)*

---

## 📂 Project Architecture

```text
Agent-MINI/
├── Agent/
│   ├── main.py              # Core execution harness, REPL, and agent loop
│   ├── memory.py            # System prompts, memory management & execution laws
│   ├── tools.py             # 14 Function tools & OpenAI function schemas
│   ├── session_manager.py   # Session persistence, loading & markdown export
│   ├── config.py            # Configuration loader and updater (setup.json)
│   ├── panelshow.py         # Rich ASCII art and command display definitions
│   ├── setup.json           # Active provider, model, and UI settings
│   └── skills/              # Domain-specific agent skills
│       ├── coding_helper.md   # Project scaffolding & timeout prevention rules
│       ├── file_operations.md # File inspection & safe editing protocols
│       ├── system_admin.md    # Windows shell commands & troubleshooting
│       └── web_research.md    # DuckDuckGo search & synthesis guidelines
├── sandbox/                 # Default isolated workspace for generated projects
├── .sessions/               # Auto-saved conversation session JSONs (git-ignored)
├── .env.example             # Template for API keys and provider endpoints
├── mini.bat                 # One-click launcher script
├── setup.bat                # One-click installation & virtual environment setup
├── pyproject.toml           # Project metadata & dependencies
├── requirements.txt         # Pip dependency manifest
└── README.md                # Comprehensive documentation
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
