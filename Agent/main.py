
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from memory import conversations
from tools import available_tools, tools

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align 

console = Console()
load_dotenv()
base_url = os.getenv("GROQ_BASE_URL")
api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(base_url = base_url, api_key = api_key)

model = "openai/gpt-oss-120b"

# ==================== LLM CALL FUCTION ===========================================================================

def call_model(messages):
    with console.status("[dim]Thinking...[/dim]", spinner="dots", spinner_style="dim"):
        responses = client.chat.completions.create(
            model=model,  
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7,
        )
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  SYSTEM : MODEL RESPONSE  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    console.print(Panel(f"[white dim]{responses}[/white dim]", title="[bold white]LLM RESPONSE[/bold white]", title_align="center", border_style="white dim"))

    return responses
# ==================================================================================================================


# ============== HEALTH CHECK FUNCTION ============================================================================
def health_check():
    # API KEY CHECK
    api_key_ok = bool(api_key)
    api_status = "[bold green]Configured[/bold green]" if api_key_ok else "[bold red]Missing[bold red]"

    # MODEL NAME
    model_ok = bool(model)
    model_status = f"[bold green]{model}[/bold green]"

    # TOOLS CHECK 
    tools_ok =bool(available_tools)
    tools_status = f"[bold green]({len(available_tools)} tools) Available[/bold green]" if tools_ok else "[bold red]Tools not configured[/bold red]"

    # OVERALL STATUS CHECK
    if api_key_ok and model_ok and tools_ok:
        overall_status = "[bold green]Healthy[/bold green]"
    else:
        overall_status = "[bold red] Issue Detected[/bold red]"
    return api_status, model_status, tools_status, overall_status
# =================================================================================================================


# ================ HERO SCREEEN PANEL =============================================================================
api_status, model_status, tools_status, overall_status = health_check()

hero_screen = f"""
[bold cyan]          Hey this is 'Agent MINI' [/bold cyan]
[italic]              Your AI Assistant [/italic]
[bold cyan]----------------------------------------------[/bold cyan]
[bold white]Agent Status: [/bold white][yellow]
        • API KEY = {api_status}
        • MODEL   = {model_status}
        • TOOLS   = {tools_status}
        • OVERALL = {overall_status}[/yellow]
[bold cyan]----------------------------------------------[/bold cyan]
[dim] 
Type '[yellow]/bye[/yellow]' or '[yellow]/exit[/yellow]' to end this conversation[/dim].
"""

console.print(Panel(Align.center(hero_screen), expand=True, border_style="bold cyan"))
# =================================================================================================================

# ============================== SESSION TOKEN DETAILS ============================================================
total_tokens_used = 0
prompt_tokens_used = 0
completion_tokens_used = 0
# =================================================================================================================


# ==================================================================================================================
def main():
    global total_tokens_used, prompt_tokens_used, completion_tokens_used
    while True:
        #print("\n")
        user_input = Prompt.ask("[bold white]YOU[/bold white]")

        if user_input.startswith("/"):
            if user_input.lower() in ["/bye", "/exit", "/cls"]:
                console.print(f"[bold yellow]See you later![/bold yellow]")
                break
            
            if user_input == "/clear":
                from memory import mem_clear
                mem_clean=mem_clear()
                console.print(f"[bold yellow]{mem_clean}[/bold yellow]")
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
                    with console.status(f"[dim]{tool_name} tool Calling...[/dim]", spinner="dots", spinner_style="dim"):
                        try:
                            tool_output = (tool_to_call(**tool_args)if tool_args else tool_to_call())
                        except TypeError:
                            tool_output = tool_to_call()
                        except Exception as e:
                            tool_output = f"Error executing tool '{tool_name}': {str(e)}"
 # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  SYSTEM : TOOL OUPUT  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        console.print(Panel(f"[white dim]Tool Name: {tool_name}\nArgument: {tool_args}\nOutput: {tool_output}[/white dim]", title="[bold white]TOOL RESPONSE[/bold white]", title_align="center", border_style="white dim"))
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
        sub_details=f"[white]Total Tokens Used:[/white] {total_tokens_used} [white]| Active Model:[/white] {active_model}"
        final_response = current_response.content or ""
        console.print(
            Panel(
                Markdown(final_response),
                title="[bold yellow]MINI[/bold yellow]",
                subtitle=f"[yellow dim]{sub_details}[/yellow dim]",
                title_align="left",
                subtitle_align="right",
                border_style="cyan"
            )
        )
        conversations.append(current_response)
# ===================================================================================================================================
if __name__ == "__main__":
    main()
# ===================================================================================================================================