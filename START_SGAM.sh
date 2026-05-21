#!/bin/bash

# ======================================================
# SGAM Media Studio Launcher & Dependency Checker
# ======================================================

echo ""
echo " [!] Checking System Requirements..."
echo ""

# 1. Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo " [X] ERROR: Python is NOT installed or NOT in your PATH."
        echo ""
        echo " Please install Python from https://www.python.org/downloads/"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# 2. Check if required folders exist
CORE_DIR="$HOME/SGAM_STMedia"
if [ ! -d "$CORE_DIR" ]; then
    echo " [!] WARNING: Core directory $CORE_DIR not found."
    echo " [!] Please ensure all system assets are in $CORE_DIR"
    echo ""
fi

# 3. Run Dependency Manager
echo " [i] Verifying Python Libraries..."
$PYTHON_CMD dependency_manager.py

# 4. Start the main application
echo ""
echo " [✓] System Ready. Starting SGAM Media Studio..."
echo ""
$PYTHON_CMD launcher.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo " [!] Application closed with an error."
    echo ""
    read -p "Press Enter to exit..."
fi
