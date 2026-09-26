
import os 
import sys
import datetime
from ddgs import DDGS 

#=====================================================
#                 TOOLS FUNCTIONS
#=====================================================
# 1. GET TIME & DATE
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d; %H:%M:%S")

# 2. WEB SEARCH
def web_search(query):
    data = DDGS().text(query, max_results=3)
    results = []
    for r in data:
        results.append({
            "title": r.get("title"),
            "url": r.get("href"),
            "snippets": r.get("body")
        }) 
    return results    

# 3. FILE READER
def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# 4. FILE WRITE / CREATE
def write_file(filepath, content):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created/written to {filepath}"
    except Exception as e:
        return f"Error Writting file: {str(e)}"

# 5. List files in the folder
def list_files(directory="."):
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error lsting directory: {str(e)}"

# 6.


#=====================================================
#                 AVAILABLE TOOLS
#=====================================================
available_tools = {
    "get_current_time" : get_current_time,
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
}


#=====================================================
#                 TOOLS DEFENITIONS
#=====================================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Use this tool only to get a current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Use this tool to get a current realworld information or anythink you don't know the answer. Trust this tool's output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Give the question to search in the Internet."}
                },
                "required": ["query"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Use this tool to read the files.",
            "parameters": {
                "type":"object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Use this tool to create or write content to a file ",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath":{"type": "string", "description": "path to the file to create/write."},
                    "content": {"type": "string", "description": "Text content to write inside the file."},
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "list_files",
            "description": "Use the tool only to List all the files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory path (default is current folder '.')"},
                },
                "required": ["directory"]
            }
        }
    }
]