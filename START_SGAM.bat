@echo off
setlocal enabledelayedexpansion

:: ======================================================
:: SGAM Media Studio Launcher & Dependency Checker
:: ======================================================

title SGAM Media Studio - System Check

echo.
echo  [!] Checking System Requirements...
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [X] ERROR: Python is NOT installed or NOT in your PATH.
    echo.
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: 2. Check if required folders exist
if not exist "C:\SGAM_STMedia" (
    echo  [!] WARNING: Core directory C:\SGAM_STMedia not found.
    echo  [!] Please ensure all system assets are in C:\SGAM_STMedia
    echo.
)

:: 3. Run Dependency Manager (Optional, if you want it to run every time)
echo  [i] Verifying Python Libraries...
python dependency_manager.py

:: 4. Start the main application
echo.
echo  [✓] System Ready. Starting SGAM Media Studio...
echo.
python launcher.py %*

if %errorlevel% neq 0 (
    echo.
    echo  [!] Application closed with an error.
    echo.
    pause
)

pause
