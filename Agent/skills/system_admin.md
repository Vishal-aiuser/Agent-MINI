# Skill: Windows System Administration & Automation

## Purpose
Use this skill when the user asks to launch applications, run system diagnostics, check network details, or manage directories and files on Windows.

## Recommended Workflow

1. **Launching Desktop Applications**
   - **Step 1:** Call `find_application(app_name)` to locate the installed application executable or `.lnk` shortcut.
   - **Step 2:** From the returned list, pass the exact path to `launch_app_by_path(app_path)`.
   - **Step 3:** Confirm to the user that the application has been launched.

2. **Running System & Network Commands (`run_terminal_cammand`)**
   - Use safe, non-interactive commands (e.g. `ipconfig`, `systeminfo`, `ping 8.8.8.8`, `git status`).
   - Avoid long-running commands that block the terminal.

3. **File & Folder Operations**
   - Check directory contents with `list_files(directory)`.
   - Create directories safely with `create_folder(folder_path)`.
   - Read and write file contents with `read_file` and `write_file`.
