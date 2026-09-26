
system_prompt="You are helpful AI Agent called 'Agent Mini', you are a brillient and friendly Assistant."

conversations = [
    {"role": "system", "content": system_prompt},
]

# ------------------- MEMORY CLEAN FUNCTION -----------------------------------------------
def mem_clear():
    conversations.clear()
    conversations.append({"role": "system", "content": system_prompt})
    return "Memory Cleared!"
# --------------------------------------------------------------------------------------------

