import os
import json 
import datetime

# .session Folder Create
SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".sessions")

def ensure_sessions_dir():
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR, exist_ok=True)

def serialize_message(msg):
    """Convert OpenAI message objects or dictionaries into json-serializable dicts."""
    if isinstance(msg, dict):
        return msg

    # OpenAI chatcompletion Message object
    res = {"role": msg.role, "content": msg.content or ""}
    if getattr(msg, "tool_calls", None):
        res["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            }
            for tc in msg.tool_calls
        ]
    return res 


def save_session(conversations, custom_title=None, existing_filename=None):
    """Saves the current conversation to a JSON file."""
    # Only system prompt irundha save panna thevailla
    user_msgs = [m for m in conversations if (m.get("role") if isinstance(m, dict) else getattr(m, "role", "")) == "user"]
    if not user_msgs:
        return None 

    ensure_sessions_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Title extraction (First user prompt from first 35 chars))
    first_prompt = user_msgs[0]["content"] if isinstance(user_msgs[0], dict) else user_msgs[0].content 
    title = custom_title or (first_prompt[:35].replace("\n", " ").strip() + ("..." if len(first_prompt) > 35 else ""))

    filename = existing_filename or f"session_{timestamp}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)

    data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "messages": [serialize_message(m) for m in conversations]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def list_sessions():
    """Returns a list of saved sessions sorted by newest first."""
    ensure_sessions_dir()
    sessions = []
    for f in os.listdir(SESSIONS_DIR):
        if f.endswith(".json") and f.startswith("session_"):
            path = os.path.join(SESSIONS_DIR, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    sessions.append({
                        "file": f,
                        "timestamp": data.get("timestamp", "Unknown"),
                        "title": data.get("title", "Untitled Session"),
                        "message_count": len(data.get("messages", []))
                    })
            except Exception:
                continue
    # Newest first
    sessions.sort(key=lambda x: x["file"], reverse=True)
    return sessions


def load_session(filename):
    """Loads a specific session file and returns the conversation list."""
    ensure_sessions_dir()
    filepath = os.path.join(SESSIONS_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("messages", [])


def export_session_markdown(conversations, filename=None):
    """Exports conversation to a clean readable Markdown file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_name = filename or f"chat_export_{timestamp}.md"
    
    md_lines = [
        f"# Agent MINI - Conversation Export",
        f"*Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "---"
    ]
    
    for msg in conversations:
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", "")
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
        
        if role == "user":
            md_lines.append(f"\n### 👤 User:\n{content}\n")
        elif role == "assistant" and content:
            md_lines.append(f"\n### 🤖 Agent MINI:\n{content}\n")
            
    with open(target_name, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    return target_name