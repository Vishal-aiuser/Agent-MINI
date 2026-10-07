
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from memory import conversations
from tools import available_tools, tools
from panelshow import show_commands


from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align 

from prompt_toolkit import PromptSession 
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style 
from prompt_toolkit import HTML



console = Console()
load_dotenv()

#####################################################  VARIABLES  ################################################################################
base_url = os.getenv("NVIDIA_BASE_URL")
api_key = os.getenv("NVIDIA_API_KEY")
model = "nvidia/nemotron-3-ultra-550b-a55b"
client = OpenAI(base_url = base_url, api_key = api_key)
reasoning_effort="medium"    # "low", "medium", or "high"


box_style = box.ASCII       # styles: box.ASCII, box.ROUNDED, box.SQUARE, box.HEAVY, box.DOUBLE, box.MINIMAL, box.HORIZONTALS, box.SIMPLE
box_color = "bold dark_orange"   # Colors: dark_orange, orange1, orange3, yellow, cyan, red, purple, green, etc,...

# ============================== SESSION TOKEN DETAILS ============================================================
total_tokens_used = 0
prompt_tokens_used = 0
completion_tokens_used = 0

###############################################################################################################################################
# ==================== LLM CALL FUCTION ===========================================================================

def call_model(messages):
    with console.status(f"[{box_color} dim]Thinking...[/{box_color} dim]", spinner="dots3", spinner_style=f"{box_color} dim"):
        responses = client.chat.completions.create(
            model=model,  
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2,
            reasoning_effort=reasoning_effort   
        )
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  SYSTEM : MODEL RESPONSE  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #console.print(Panel(f"[white dim]{responses}[/white dim]", title="[bold white]LLM RESPONSE[/bold white]", title_align="center", border_style="white dim"))

    return responses
# ==================================================================================================================


# ============== HEALTH CHECK FUNCTION ============================================================================
def health_check():
    # API KEY CHECK
    api_key_ok = bool(api_key)
    api_status = "[green]Configured[/green]" if api_key_ok else "[red]Missing[red]"

    # MODEL NAME
    model_ok = bool(model)
    model_status = f"[green]{model}[/green]"

    # TOOLS CHECK 
    tools_ok =bool(available_tools)
    tools_status = f"[green]({len(available_tools)} tools) Available[/green]" if tools_ok else "[red]Tools not configured[/red]"

    # OVERALL STATUS CHECK
    if api_key_ok and model_ok and tools_ok:
        overall_status = "[green]Healthy[/green]"
    else:
        overall_status = "[red] Issue Detected[/red]"
    return api_status, model_status, tools_status, overall_status
# =================================================================================================================
# Frame Box
def console_box(content):
    console.print(Panel(f"{content}",title="[dark_orange]MINI[/dark_orange]", title_align="left", border_style=box_color,box=box_style, expand="True"))

# ================ HERO SCREEEN PANEL =============================================================================
api_status, model_status, tools_status, overall_status = health_check()

hero_screen = f"""
[dark_orange]          Hey! this is 'Agent MINI' [/dark_orange]
[italic]              Your AI Assistant [/italic]
[{box_color}]----------------------------------------------[/{box_color}][bold white]
        • API KEY = {api_status}
        • MODEL   = {model_status}
        • TOOLS   = {tools_status}
        • OVERALL = {overall_status}[/bold white]
[{box_color}]----------------------------------------------[/{box_color}]
[dim] 
Type '[purple]/bye[/purple]' or '[purple]/exit[/purple]' to end this conversation
            '[purple]/help[/purple]' for all commands.
[/dim]
"""

console.print(Panel(Align.center(hero_screen), expand=True, border_style=box_color, box=box_style))
# =================================================================================================================

# =================================================================================================================

prompt_style = Style.from_dict({
    "completion-menu": "bg:#2b2b2b #ffffff",
    "completion-menu.completion.current": "bg:#ff8c00 #000000 bold",
    "completion-menu.completion": "bg:#2b2b2b #ffb86c",
    "scrollbar.background": "bg:#1e1e1e",
    "scrollbar.button": "bg:#ff8c00",
})
class SlashCommandCompleter(Completer):
    def __init__(self, command):
        self.commands = command
    
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor 
        if text_before_cursor.startswith("/"):
            for cmd in self.commands:
                if cmd.lower().startswith(text_before_cursor.lower()):
                    yield Completion(
                        text=cmd,
                        start_position=-len(text_before_cursor)
                    )

commands_list = ["/bye", "/clear", "/help", "/effort"]
command_completer = SlashCommandCompleter(commands_list)

session = PromptSession(
    history=InMemoryHistory(),
    completer=command_completer,
    style=prompt_style
)

# ==================================================================================================================
def main():
    
    global total_tokens_used, prompt_tokens_used, completion_tokens_used, reasoning_effort

    while True:
        #print("\n")
        user_input = session.prompt("YOU ❯ ")

        if user_input.startswith("/"):
            if user_input.lower() in ["/bye", "/exit", "/cls"]:
                console_box("See you Later!..👋")
                break
            
            if user_input == "/clear":
                confirm_input = Prompt.ask("[dark_orange]MINI: [/dark_orange]Are you sure to clear this Chat Memory? (Y/N)")
                if confirm_input.lower() == "y":
                    from memory import mem_clear
                    mem_clean=mem_clear()
                    console_box(mem_clean)
                    continue
                else:
                    console_box("Memory Cleaning Cancelled!")
                    continue
            if user_input.lower() == "/help":
                console_box(show_commands)
                continue

            if user_input.lower().startswith("/effort"):
                if user_input.lower() == "/effort low":
                    reasoning_effort = "low"
                    console_box("Effort level changed to 'low'.")
                    continue
                elif user_input.lower() == "/effort medium":
                    reasoning_effort = "meduim"
                    console_box("Effort level changed to 'medium'.")
                    continue
                elif user_input.lower() == "/effort high":
                    reasoning_effort = "high"
                    console_box("Effort level changed to 'high'.")
                    continue
                else:
                    console_box("Available Efforts: 'low', 'medium', 'high', (e.g. \"/effort medium\")")
                    continue

        if not user_input.strip():
            console_box("Ask Anythink...")
            continue
        
        conversations.append({"role": "user", "content": user_input})
        model_response = call_model(messages=conversations)
        # ------------------ APPEND TOKENS DETAILS ---------------------------------
        total_tokens_used += model_response.usage.total_tokens
        prompt_tokens_used += model_response.usage.prompt_tokens 
        completion_tokens_used += model_response.usage.completion_tokens
        active_model=model_response.model
        # --------------------------------------------------------------------------
        current_response = model_response.choices[0].message

 # ========================== TOOL CALL ACTIONS ========================================================================================================
       # tool_step_count = 0
      #  max_tool_steps = 4
        while current_response.tool_calls: #and tool_step_count < max_tool_steps:
            #tool_step_count += 1
            conversations.append(current_response)

            for tool_call in current_response.tool_calls:
                tool_name = tool_call.function.name
                tool_to_call = available_tools.get(tool_name)
                tool_args = json.loads(tool_call.function.arguments)
                tool_args = {k: v for k, v in tool_args.items() if k != ""}

                if tool_to_call:
                    with console.status(f"[{box_color} dim]{tool_name} Tool Calling...[/{box_color} dim]", spinner="star", spinner_style=f"{box_color} dim"):
                        try:
                            tool_output = (tool_to_call(**tool_args)if tool_args else tool_to_call())
                        except TypeError:
                            tool_output = tool_to_call()
                        except Exception as e:
                            tool_output = f"Error executing tool '{tool_name}': {str(e)}"
 # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  SYSTEM : TOOL OUPUT  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        #console.print(Panel(f"[white dim]Tool Name: {tool_name}\nArgument: {tool_args}\nOutput: {tool_output}[/white dim]", title="[bold white]TOOL RESPONSE[/bold white]", title_align="center", border_style="white dim"))
                        #console.print(Panel(f"[white dim]Tool Name: {tool_name}", title="[bold white]TOOL RESPONSE[/bold white]", title_align="center", border_style="white dim"))

 # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        conversations.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(tool_output),
                        })

            model_response = call_model(messages=conversations)
        # ------------------ APPEND TOKENS DETAILS ---------------------------------
            total_tokens_used += model_response.usage.total_tokens
            prompt_tokens_used += model_response.usage.prompt_tokens 
            completion_tokens_used += model_response.usage.completion_tokens
            active_model=model_response.model
        # --------------------------------------------------------------------------
            current_response = model_response.choices[0].message

# =================== AGENT's FINAL RESPONSE =====================================================================
        sub_details=f"[dim][white]Tokens Used:[/white] {total_tokens_used} [white]| Model:[/white] {active_model} [white]| Effort:[/white] {reasoning_effort}[dim]"
        final_response = current_response.content or ""
        console.print(
            Panel(
                Markdown(final_response),
                title="[dark_orange]MINI[/dark_orange]",
                subtitle=f"[orange3]{sub_details}[/orange3]",
                title_align="left",
                subtitle_align="right",
                border_style=box_color,
                box=box_style
            )
        )
        conversations.append(current_response)
# ===================================================================================================================================
if __name__ == "__main__":
    main()
# ===================================================================================================================================