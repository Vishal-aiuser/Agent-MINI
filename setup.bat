@echo off
echo ===================================================
echo             Agent MINI - Setup
echo ===================================================

:: 1. uv install aagi irukka nu check pannuvom
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'uv' is not installed!
    echo Please install uv first: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo ===================================================
    pause
    exit /b
)

:: 2. Dependencies sync & venv auto-creation
echo [1/3] Creating virtual environment and installing packages...
uv sync
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages.
    pause
    exit /b
)

:: 3. .env file create pannuvom (illana)
echo [2/3] Checking .env configuration...
if not exist .env (
    echo [INFO] Creating new .env file...
    (
        echo # API Configuration
        echo GROQ_BASE_URL="https://api.groq.com/openai/v1"
        echo GROQ_API_KEY=""
        echo NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
        echo NVIDIA_API_KEY=""
    ) > .env
    echo [NOTE] Created .env file. Please add your API Keys in .env!
) else (
    echo [INFO] .env file already exists.
)

:: 4. Done message
echo ===================================================
echo [3/3] Setup completed successfully!
echo.
echo Next steps:
echo 1. Open '.env' file and paste your API Key.
echo 2. Double click 'mini.bat' to start the agent!
echo ===================================================
pause
