
system_prompt = (
    "You are a helpful AI Agent called 'Agent Mini'. "
    "You have access to specific tools. "
    "CRITICAL RULE: You must ONLY call tools that are explicitly provided in the tools list. "
    "NEVER call or invent any unlisted tools like 'commentary' or thoughts."
)

conversations = [
    {"role": "system", "content": system_prompt},
]

# ------------------- MEMORY CLEAN FUNCTION -----------------------------------------------
def mem_clear():
    conversations.clear()
    conversations.append({"role": "system", "content": system_prompt})
    return "Memory Cleared!"
# --------------------------------------------------------------------------------------------

