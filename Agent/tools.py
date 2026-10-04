
import os 
import sys
import datetime
import subprocess
import httpx
from bs4 import BeautifulSoup
from ddgs import DDGS 

#=====================================================
#                 TOOLS FUNCTIONS
#=====================================================
# 1. GET TIME & DATE
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d; %H:%M:%S")

# 2. WEB SEARCH
def web_search(query):
    try:
        data = DDGS().text(query, max_results=3)
        results = []
        for r in data:
            results.append({
                "title": r.get("title"),
                "url": r.get("href"),
                "snippets": r.get("body")
            }) 
        return results if results else "No results found for this search query."
    except Exception as e:
        return f"Search error or no results: {str(e)}"
         

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

# 6. Create Creator
def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        return f"Successfully created folder: {folder_path}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

# 7. Python code Runner
def run_python_code(code):
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        if not output.strip():
            output = "Code executed successfully with no output."
        return output
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (30 seconds limit)."
    except Exception as e:
        return f"Error running code: {str(e)}"

# 8. FIND APPLICATION PATH
def find_application(app_name):
    app_name_lower = app_name.lower().strip()
    search_dirs = [
        os.path.expandvars(r"%APPDATA\Microsoft\Windows\Start menu\Programs"),
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"~\Desktop"),
        os.path.expandvars(r"%PUBLIC%\Desktop"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramFiles(x86)%"),
    ]

    matches = []
    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            depth = root[len(base_dir):].count(os.sep)
            if depth > 3:
                continue
            for file in files:
                if file.lower().endswith(('.lnk', '.exe')):
                    name_without_ext = os.path.splitext(file)[0].lower()
                    if app_name_lower in name_without_ext:
                        full_path = os.path.join(root,file)
                        if full_path not in matches:
                            matches.append(full_path)
    if matches:
        return matches[:5]
    return f"No installed application found matching '{app_name}'."


# 9. LAUNCH APPLICATION BY PATH
def launch_app_by_path(app_path):
    try:
        if not os.path.exists(app_path):
            return f"Error: File path does not exists: {app_name}"
        os.startfile(app_path)
        return f"Successfully launched: {app_path}"
    except Exception as e:
        try:
            subprocess.Popen([app_path], shell=True)
            return f"Successully launched via fallback: {app_path}"
        except Exception as err:
            return f"Error launching application: {str(err)}"


# 10. Web Scraper
def scrape_webpage(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        with httpx.Client(headers=headers, timeout=15, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Scripts, styles, nav, footer thevaillaatha elements-ah remove pannuvom
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.decompose()
        # Clean text mattum eduppom
        text = soup.get_text(separator="\n", strip=True)
        # Token limit save panna first 4000 characters limit
        if len(text) > 4000:
            text = text[:4000] + "\n\n...[Content truncated for token length]..."
        return text if text else "No readable content found on this webpage."
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


# 11. TERMINAL / SHELL COMMAND RUNNER
def run_terminal_cammand(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            errors="replace"
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[Error / Warnings]:\n{result.stderr}"
        if not output.strip():
            output = f"Command executed successfully with no output."
        return output
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out (60 seconds limit)."
    except Exception as e:
        return f"Error executing command: {str(e)}"


# 12. SKILL READER
skills_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")
def read_skill(skill_name):
    try:
        filename = skill_name if skill_name.endswith(".md") else f"{skill_name}.md"
        filepath = os.path.join(skills_dir, filename)

        if not os.path.exists(filepath):
            available = [f.replace(".md", "") for f in os.listdir(skills_dir) if f.endswith(".md")]
            return f"Skill '{skill_name}' not found. Available skills: {available if available else 'None'}"
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading skill '{skill_name}': {str(e)}"


# 13. PDF CREATOR
from fpdf import FPDF 

def create_pdf(filepath, content, title="Document"):
    try:
        if not filepath.lower().endswith(".pdf"):
            filepath += ".pdf"
            
        parent_dir = os.path.dirname(filepath)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Unicode special characters & dashes cleanup (No more '?' in words)
        replacements = {
            "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2015": "-", "\u2212": "-",
            "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
            "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
            "\u2022": "-", "\u2023": "-", "\u2043": "-", "\u2026": "..."
        }
        for k, v in replacements.items():
            content = content.replace(k, v)
            if title:
                title = title.replace(k, v)
                
        content = content.encode("latin-1", "replace").decode("latin-1")
        if title:
            title = title.encode("latin-1", "replace").decode("latin-1")

        # Main Document Title
        if title:
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.cell(0, 10, text=title, new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(5)

                # Body Content with clean Headings & Markdown Bold
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(3)
                continue
            
            # new_x="LMARGIN", new_y="NEXT" potta thaan adutha line left margin-ku reset aagum!
            if line.startswith("### "):
                pdf.set_font("Helvetica", style="B", size=12)
                pdf.multi_cell(0, 7, text=line[4:], markdown=True, new_x="LMARGIN", new_y="NEXT")
            elif line.startswith("## "):
                pdf.ln(2)
                pdf.set_font("Helvetica", style="B", size=13)
                pdf.multi_cell(0, 7, text=line[3:], markdown=True, new_x="LMARGIN", new_y="NEXT")
            elif line.startswith("# "):
                pdf.ln(3)
                pdf.set_font("Helvetica", style="B", size=15)
                pdf.multi_cell(0, 8, text=line[2:], markdown=True, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_font("Helvetica", size=10)
                pdf.multi_cell(0, 6, text=line, markdown=True, new_x="LMARGIN", new_y="NEXT")

        pdf.output(filepath)
        return f"Successfully created PDF: {os.path.abspath(filepath)}"
    except Exception as e:
        return f"Error creating pdf: {str(e)}"

        

#=====================================================
#                 AVAILABLE TOOLS
#=====================================================
available_tools = {
    "get_current_time" : get_current_time,
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "create_folder":  create_folder,
    "run_python_code": run_python_code,
    "find_application": find_application,
    "launch_app_by_path": launch_app_by_path,
    "scrape_webpage": scrape_webpage,
    "run_terminal_cammand": run_terminal_cammand,
    "read_skill": read_skill,
    "create_pdf": create_pdf,
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
    },
    {
        "type": "function",
        "function": {
            "name": "create_folder",
            "description": "Use this tool to create a new folder or directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {"type": "string", "description": "path or name of the folder to create."}
                },
                "required": ["folder_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Execute Python code and get the console output or error messages. Use print() in the code to get output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The Python code string to execute."}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_application",
            "description": "Search the system for an installed application or shortcut by name and return its exact file paths.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the application to find (e.g. 'whatsapp', 'chrome', 'free fire', 'vscode')."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "launch_app_by_path",
            "description": "Launch an application using its exact path found from find_application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_path": {"type": "string", "description": "The exact full path of the application executable or shortcut to open."}
                },
                "required": ["app_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_webpage",
            "description": "Scrape and read the full text content from a specific website URL. Use this after web_search to read the actual page content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The full HTTP/HTTPS URL of the website to scrape."}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_cammand",
            "description": "Execute a Windows shell/terminal command (e.g. 'ipconfig', 'ping 8.8.8.8', 'systeminfo', 'git status') and return the console output.",
            "parameters": {
                "type": "object",
                "properties":{
                    "command": {"type": "string", "description": "The exact shell command line string to run."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "Read step-by-step guidelines and workflows from a skill markdown file in the skills folder before performing complex tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "description": "Name of the skill to read (e.g. 'web_research', 'coding_helper', 'system_admin')."}
                },
                "required": ["skill_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_pdf",
            "description": "Create a formatted PDF document with a title and text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path or file name of the PDF to create (e.g. 'ai_report.pdf' or 'notes/summary.pdf')."},
                    "content": {"type": "string", "description": "Text content to write inside the PDF body."},
                    "title": {"type": "string", "description": "Title for the document header (e.g. 'AI Research Report')."},
                },
                "required": ["filepath", 'content']
            }
        }
    }
]