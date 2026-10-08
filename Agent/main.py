
import os
import json
import time
from config import load_config, update_config
from openai import OpenAI, InternalServerError, NotFoundError, APITimeoutError
from dotenv import load_dotenv
from memory import conversations
from tools import available_tools, tools
from panelshow import show_commands, logo_art

from rich import box
from rich.table import Table
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


BOX_STYLES = {
    "ASCII": box.ASCII,
    "ROUNDED": box.ROUNDED,
    "SQUARE": box.SQUARE,
    "HEAVY": box.HEAVY,
    "DOUBLE": box.DOUBLE,
    "MINIMAL": box.MINIMAL,
    "HORIZONTALS": box.HORIZONTALS,
    "SIMPLE": box.SIMPLE
}

# Config load
config = load_config()
model = config.get("model")
box_color = config.get("box_color")
box_style = BOX_STYLES.get(config.get("box_style"), box.ASCII)
reasoning_effort = config.get("reasoning_effort")

configured_provider = config.get("provider")
base_url = os.getenv(f"{configured_provider.upper()}_BASE_URL")
api_key = os.getenv(f"{configured_provider.upper()}_API_KEY")


client = OpenAI(base_url = base_url, api_key = api_key)

# ============================== SESSION TOKEN DETAILS ============================================================
total_tokens_used = 0
prompt_tokens_used = 0
completion_tokens_used = 0

# ===============================================================================================================================================================
# Frame Box
def console_box(content):
    console.print(Panel(f"{content}",title="[dark_orange]MINI[/dark_orange]", title_align="left", border_style=box_color,box=box_style, expand="True"))

# SYSTEM Message
def sys_message(content, color="red"):
    console.print(f"[{color}][SYSTEM: {content}][/{color}]")

###############################################################################################################################################
# ==================== LLM CALL FUCTION ===========================================================================

def call_model(messages, retries=5):
    for attempt in range(retries + 1):
        try:
            with console.status(f"[{box_color} dim]Thinking...[/{box_color} dim]", spinner="dots3", spinner_style=f"{box_color} dim"):
                responses = client.chat.completions.create(
                    model=model,  
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.2,
                    reasoning_effort=reasoning_effort,
                    timeout=90.0   
                )
 # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  SYSTEM : MODEL RESPONSE  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                #console.print(Panel(f"[white dim]{responses}[/white dim]", title="[bold white]LLM RESPONSE[/bold white]", title_align="center", border_style="white dim"))
            return responses
        except InternalServerError:
            if attempt < retries:
                time.sleep(2)
                sys_message(f"Retrying connection... ({attempt+1}/{retries})")
                continue 
            return None
        except NotFoundError:
            sys_message("Model Not Found")
            return None
        except APITimeoutError:
            if attempt < retries:
                time.sleep(2)
                sys_message(f"Request timed out. Retrying... ({attempt+1}/{retries})")
                continue
            sys_message("Request timed out (90s limit reached).")
            return None
        except Exception as e:
            sys_message(f"{str(e)}")
            return None
    return None
# ==================================================================================================================


# ============== HEALTH CHECK FUNCTION ============================================================================
def health_check():
    # PROVIDER CHECK
    provider_ok = bool(api_key)
    provider_status = f"[green]{configured_provider}[/green]" if provider_ok else "[red]Provider Missing[/red]"

    # API KEY CHECK
    api_key_ok = bool(api_key)
    api_status = "[green]Configured[/green]" if api_key_ok else "[red]Missing[/red]"

    # MODEL NAME
    model_ok = bool(model)
    model_status = f"[green]{model}[/green]"

    # TOOLS CHECK 
    tools_ok =bool(available_tools)
    tools_status = f"[green]({len(available_tools)} tools) Available[/green]" if tools_ok else "[red]Tools not configured[/red]"

    # OVERALL STATUS CHECK
    if provider_ok and api_key_ok and model_ok and tools_ok:
        overall_status = "[green]Healthy[/green]"
    else:
        overall_status = "[red] Issue Detected[/red]"
    return provider_status, api_status, model_status, tools_status, overall_status
# =================================================================================================================

# ================ HERO SCREEEN PANEL =============================================================================

provider_status, api_status, model_status, tools_status, overall_status = health_check()

status_text = f"""
[white bold]                  Your AI Agent [/white bold]
[{box_color}] ----------------------------------------------[/{box_color}][bold white]
         • PROVIDER = {provider_status}
         • API KEY  = {api_status}
         • MODEL    = {model_status}
         • TOOLS    = {tools_status}
         • OVERALL  = {overall_status}[/bold white]
[{box_color}] ----------------------------------------------[/{box_color}]
[dim] 
Type '[purple]/bye[/purple]' or '[purple]/exit[/purple]' to end this conversation
            '[purple]/help[/purple]' for all commands.
[/dim]
"""

console.print(Panel(Align.center(f"[{box_color}]{logo_art}[/{box_color}]"+status_text), expand=True, border_style=box_color, box=box_style))

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

commands_list = ["/bye", "/clear", "/help", "/effort", "/model", "/color", "/provider"]
command_completer = SlashCommandCompleter(commands_list)

session = PromptSession(
    history=InMemoryHistory(),
    completer=command_completer,
    style=prompt_style
)

# ==================================================================================================================
def main():
    
    global client, total_tokens_used, prompt_tokens_used, completion_tokens_used, reasoning_effort, box_color, model, base_url, api_key

    while True:
        #print("\n")
        user_input = session.prompt("YOU ❯ ")

        # Command filter
        if user_input.startswith("/"):
            if user_input.lower() in ["/bye", "/exit", "/cls"]:
                console_box("See you Later!..👋")
                break
            
            # Chat memory Clear command:
            if user_input == "/clear":
                confirm_input = Prompt.ask("[dark_orange]MINI: [/dark_orange]Are you sure to clear this Chat Memory? (Y/N)")
                if confirm_input.lower() == "y":
                    from memory import mem_clear
                    mem_clean=mem_clear()
                    total_tokens_used = 0
                    prompt_tokens_used = 0 
                    completion_tokens_used = 0
                    sys_message(mem_clean,"green")
                    continue
                else:
                    sys_message("Memory Cleaning Cancelled!")
                    continue
            
            # Help Command
            if user_input.lower() == "/help":
                console_box(show_commands)
                continue

            # Effor change Command:
            if user_input.startswith("/effort"):
                if user_input == "/effort low":
                    reasoning_effort = "low"
                    update_config("reasoning_effort", reasoning_effort)
                    console_box("Effort level changed to 'low'.")
                    continue
                elif user_input == "/effort medium":
                    reasoning_effort = "medium"
                    update_config("reasoning_effort", reasoning_effort)
                    console_box("Effort level changed to 'medium'.")
                    continue
                elif user_input == "/effort high":
                    reasoning_effort = "high"
                    update_config("reasoning_effort", reasoning_effort)
                    console_box("Effort level changed to 'high'.")
                    continue
                else:
                    sys_message("Available Efforts: 'low', 'medium', 'high', (e.g. \"/effort medium\")")
                    continue

            # Box Color change command:
            if user_input.lower().startswith("/color"):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 2:
                    new_color = parts[1]
                    box_color = new_color
                    update_config("box_color", new_color)
                    sys_message(f"Theme color saved as: '{new_color}'", "green")
                    continue 
                else:
                    sys_message(f"Invalid Color Command. (Try: e.g. '/color bold red')")
                    continue
            
            # Change Provider
            if user_input.lower().startswith("/provider"):
                parts = user_input.split(maxsplit=1)
                if len(parts) >1:
                    new_provider = parts[1].lower()
                    if new_provider == "groq":
                        base_url = os.getenv("GROQ_BASE_URL")
                        api_key = os.getenv("GROQ_API_KEY")
                        update_config("provider", "groq")
                        client = OpenAI(base_url=base_url, api_key=api_key)
                        sys_message("Provider changed as 'groq'.", "green")
                        continue
                    if new_provider in ["nvidia", "nvidia nim", "nvidia_nim", "nvidia-nim"]:
                        base_url = os.getenv("NVIDIA_BASE_URL")
                        api_key = os.getenv("NVIDIA_API_KEY")
                        update_config("provider", "nvidia")
                        client = OpenAI(base_url=base_url, api_key=api_key)
                        sys_message("Provider changed as 'nvidia.'", "green")
                        continue
                    if new_provider in ["custom_provider", "custom provider", "custom-provider"]:
                        base_url = os.getenv("CUSTOM_PROVIDER_BASE_URL")
                        api_key = os.getenv("CUSTOM_PROVIDER_API_KEY")
                        update_config("provider", "custom_provider")
                        client = OpenAI(base_url=base_url, api_key=api_key)
                        sys_message("Provider changed as 'custom_provider'.", "green")
                        continue 
                    else:
                        sys_message("Invalid Provider. (Valid Providers: 'groq', 'nvidia', 'custom').")
                        continue
                else:
                    sys_message("Invalid Provider. (Valid Providers: 'groq', 'nvidia', 'custom').")
                    continue


            # Model Change Command:
            if user_input.startswith("/model"):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 2:
                    new_model = parts[1].strip()
                    model = new_model
                    update_config("model", new_model)
                    sys_message(f"Model permanently changed to: '{new_model}'", "green")
                    continue 
                else:
                    sys_message(f"Type '/model <model_name>' (e.g., /model qwen/qwen3.8-27b)")
                    continue 

        # Empty Prompt:
        if not user_input.strip():
            console_box("Ask Anythink...")
            continue
        
        conversations.append({"role": "user", "content": user_input})
        model_response = call_model(messages=conversations)
        if not model_response:
            continue
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
                        console.print(f"[dim] > '{tool_name.upper()}' Tool called[/dim]")
 # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        conversations.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(tool_output),
                        })

            model_response = call_model(messages=conversations)
            if not model_response:
                break
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
                title=f"[bold {box_color}]MINI[/bold {box_color}]",
                subtitle=f"[{box_color} dim]{sub_details}[/{box_color} dim]",
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