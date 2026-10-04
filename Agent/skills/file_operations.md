# Skill: Safe File & Folder Operations with Confirmation and Verification

## Purpose
Use this skill whenever creating, writing, or modifying files, folders, or PDF documents. This ensures no data is accidentally overwritten, guarantees that files are saved in the user's intended location, and verifies data integrity.

## Mandatory Step-by-Step Workflow

### Step 1: Check Target Directory (Ask if Unspecified)
- Check whether the user specified a target folder or directory (e.g., `sandbox/`, `notes/`, `Desktop/`).
- **If the user DID NOT specify a directory:**
  - Do NOT create the file in a random location.
  - Ask the user politely: 
    *"Where would you like me to save this file? (e.g., inside the 'sandbox' folder or the current directory?)"*
  - Wait for their choice or proceed only when the target directory is clear.

### Step 2: Check for Existing Files (Prevent Accidental Overwrite)
- Call `list_files(directory)` on the target directory.
- Check if a file or folder with the requested name already exists.
- **If the file already exists:**
  - Do NOT overwrite it immediately.
  - Warn the user and ask for confirmation:
    *"A file named '[filename]' already exists in '[directory]'. Would you like me to replace/overwrite it, or save it with a new name (e.g., '[filename_v2]')?"*
  - Follow the user's explicit decision.

### Step 3: Create the File or Folder
Once the directory and confirmation are established:
- **For Folders:** Call `create_folder(folder_path)`.
- **For Text/Code Files:** Call `write_file(filepath, content)`.
- **For PDF Documents:** Call `create_pdf(filepath, content, title)`.

### Step 4: Mandatory Verification
Never finish a task without checking the created file:
- **Verify Text/Code Files:** Call `read_file(filepath)` to confirm that the text was written accurately and completely.
- **Verify Folders:** Call `list_files(directory)` to confirm the folder exists.
- **Verify PDFs:** Check the tool response and file presence to ensure error-free creation.

### Step 5: Final Response with Exact Location
In the final message to the user:
- Confirm that the file/folder has been successfully created **and verified**.
- Always state the **exact location / full path** of the file so the user can easily find it:
  ```text
  File created and verified successfully!
  Location: C:\Users\VISHAL\Desktop\Agent-Mini\sandbox\notes.txt
  ```
