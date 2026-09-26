# AGENT MINI

**MINI** is an interactive, tool-augumented CLI AI Agent, powered by the **Groq API**.

---

## ✨ Features

- **⚡ Fast Inference**: Built on top of Groq's high-speed LLM models.
- **🛠️ Agent Tools**:
    - **Live Web Search** (via `ddgs` DuckDuckGo search)
    - **File Operations** (Read, Write, List directory files)
- **🎨 Rich Terminal UI**: Interactive terminal interface displaying health status, live response styling, token usage counters, and panel views.
- **💬 Chat History & Memory**: Save session history or clear conversation context at any time.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- A [Groq API Key](https://console.groq.com/keys)

### 2. Installation

Clone the repository and navigate into the folder:
```bash
git clone https://github.com/Vishal-aiuser/Agent-MINI.git
cd Agent-MINI
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

*(Or if you use `uv`)*:
```bash
uv sync
```

### 3. Environment Setup

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🏃 Usage

Run the agent script:
```bash
.\mini.bat
```

*(Or double click the `mini.bat` file in the folder)*

### 💡 Available Commands inside CLI
- `/clear` - Clear current conversation memory
- `/exit` / `/bye` - Exit the agent CLI

---

## 📂 Project Structure

```text
.
├── Agent/
│   ├── main.py       # Main AI Agent entry point & CLI logic
│   ├── memory.py      # Conversation state & prompt management
│   └── tools.py       # Tool definitions 
├── .env.example       # Environment template
├── pyproject.toml     # Project dependencies & build config
├── requirements.txt   # Python package dependencies
└── README.md          # Project documentation
```

---
