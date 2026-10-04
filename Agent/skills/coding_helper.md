# Skill: Python Coding & Execution

## Purpose
Use this skill when the user asks to write, test, debug, or execute Python scripts and calculations.

## Recommended Workflow

1. **Plan Before Writing**
   - Identify inputs, required packages (prefer standard library or installed packages), and desired output format.

2. **Run Quick Scripts / Tests (`run_python_code`)**
   - Write clean, self-contained Python code.
   - Always include `print()` statements to display the calculated result or outputs.
   - Call `run_python_code(code)` to verify that it executes without errors.

3. **Handle Errors Iteratively**
   - If execution returns an error in `[Errors]`, analyze the traceback carefully.
   - Fix the logic or syntax and test again before answering.

4. **Saving Persistent Code (`write_file`)**
   - If the user asked to create a script file (e.g. `test.py` or `app.py`), call `write_file(filepath, content)`.
