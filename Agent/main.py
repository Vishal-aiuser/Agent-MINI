
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
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style 
from prompt_toolkit import HTML



console = Console()
load_dotenv()

#####################################################  VARIABLES  ################################################################################
base_url = os.getenv("GROQ_BASE_URL")
api_key = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-120b"
client = OpenAI(base_url = base_url, api_key = api_key)

box_style = box.ASCII
box_color = "dark_orange"
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
            temperature=0.7,
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


# ================ HERO SCREEEN PANEL =============================================================================
api_status, model_status, tools_status, overall_status = health_check()

hero_screen = f"""
[dark_orange]          Hey! this is 'Agent MINI' [/dark_orange]
[italic]              Your AI Assistant [/italic]
[{box_color}]----------------------------------------------[/{box_color}]
[bold white]Agent Status: [/bold white][yellow]
        • API KEY = {api_status}
        • MODEL   = {model_status}
        • TOOLS   = {tools_status}
        • OVERALL = {overall_status}[/yellow]
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
command_completer = WordCompleter(
        ["/bye", "/exit", "/clear", "/help"],
        ignore_case=True
    )

session = PromptSession(
    history=InMemoryHistory(),
    completer=command_completer,
    style=prompt_style
)

# ==================================================================================================================
def main():
    
    global total_tokens_used, prompt_tokens_used, completion_tokens_used

    while True:
        #print("\n")
        user_input = session.prompt("YOU ❯ ")

        if user_input.startswith("/"):
            if user_input.lower() in ["/bye", "/exit", "/cls"]:
                console.print(Panel(f"See you later!",title="[dark_orange]MINI[/dark_orange]", title_align="left", border_style=box_color,box=box_style, expand="True"))
                break
            
            if user_input == "/clear":
                confirm_input = Prompt.ask("[dark_orange]MINI: [/dark_orange]Are you sure to clear this Chat Memory? (Y/N)")
                if confirm_input.lower() == "y":
                    from memory import mem_clear
                    mem_clean=mem_clear()
                    console.print(Panel(f"{mem_clean}",title="[dark_orange]MINI[/dark_orange]", title_align="left", border_style=box_color,box=box_style, expand="True"))
                    continue
                else:
                    console.print(Panel(f"Memory Clean cancelled!",title="[dark_orange]MINI[/dark_orange]", title_align="left", border_style=box_color,box=box_style, expand="True"))
                    continue
            if user_input == "/help":
                console.print(f"{show_commands}")
                continue

            

        if not user_input.strip():
            console.print(f"[bold yellow]Ask Anything..[/bold yellow]")
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
        sub_details=f"[dim][white]Total Tokens Used:[/white] {total_tokens_used} [white]| Active Model:[/white] {active_model}[dim]"
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