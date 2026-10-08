import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "setup.json")

DEFAULT_CONFIG = {
    "provider": "groq",
    "model": "nvidia/nemotron-3-ultra-550b-a55b",
    "reasoning_effort": "medium",
    "box_color": "dark_orange",
    "box_style": "ASCII"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def update_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
