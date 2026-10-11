# Skill: Coding, Development & Project Scaffolding

## Purpose
Use this skill whenever the user requests writing code, building software, designing web pages (HTML/CSS/JS), developing scripts, or scaffolding full project applications.

---

## 🚨 MANDATORY WORKSPACE & ISOLATION LAWS

### 1. Default Workspace: `sandbox/`
- By default, **ALL project creations MUST happen inside the `sandbox/` directory.**
- **Project Subfolder:** Always scaffold projects inside a dedicated project subfolder (e.g., `create_folder("sandbox/portfolio")`).
- **NEVER** write files directly in the root directory.

---

## ⚡ SEQUENTIAL FILE-BY-FILE GENERATION (STABLE & FAST)

### ⚠️ CRITICAL EXECUTION RULES:
- **ONE COMPLETE FILE PER TOOL CALL:** DO NOT generate empty dummy files, and DO NOT leave empty `<body></body>` tags. Each file must be written completely with production-ready content.
- **DO NOT combine multiple files in one turn:** Write HTML first, then CSS in the next turn, then JS in the next turn.

---

## 🛠️ Step-by-Step Execution Sequence

### Step 1: Create Dedicated Folder
- Create the project folder inside sandbox:
  `create_folder("sandbox/<project_name>")`

### Step 2: Write Complete `index.html`
- Call `write_file("sandbox/<project_name>/index.html", content)` with FULL, production-ready HTML:
  - Doctype, `<head>`, meta tags, Google Fonts, and link to `style.css`.
  - Rich `<body>` content: Navigation bar, Hero section, Feature/Service cards, About/Bio, Testimonials, Contact details, Footer, and `<script src="script.js"></script>`.
  - NEVER leave empty tags or placeholder comments.

### Step 3: Write Complete `style.css`
- In the next step, call `write_file("sandbox/<project_name>/style.css", content)` with FULL, modern styling:
  - CSS reset, custom color variables (HSL / sleek dark mode or vibrant palette).
  - Modern typography, flexbox/grid layouts, card styling, hover animations, buttons.
  - Fully responsive media queries (`@media (max-width: 768px)`).

### Step 4: Write Complete `script.js`
- In the next step, call `write_file("sandbox/<project_name>/script.js", content)` with complete interactivity:
  - Mobile hamburger toggle, smooth scrolling, interactive modals, form validation, dynamic filter effects.

### Step 5: (Optional) Append Extra Sections
- If you need to extend an existing file with extra modules or logs, use `append_file`.

### Step 6: Delivery & Summary
- Once all files are written, output a clean markdown summary:
  - Directory path: `sandbox/<project_name>/`
  - Created files: `index.html`, `style.css`, `script.js`
  - How to open and preview the site in a browser.

