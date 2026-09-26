
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

# 3. 
#=====================================================
#                 AVAILABLE TOOLS
#=====================================================
available_tools = {
    "get_current_time" : get_current_time,
    "web_search": web_search,
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
                    "query": {
                        "type": "string", "description": "Give the question to search in the Internet."
                    }
                },
                "required": ["query"],
            }
        }
    },
]