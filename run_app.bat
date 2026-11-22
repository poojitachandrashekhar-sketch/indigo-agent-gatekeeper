@echo off
title IndiGo Agent Gatekeeper - AI Governance Prototype
echo =========================================================================
echo    IndiGo Airlines - AI Agent Gatekeeper Prototype
echo    MBA Course: AI Agent Governance and Security
echo =========================================================================
echo.
echo Launching your local Streamlit dashboard...
echo Once started, your web browser will open automatically at:
echo http://localhost:8501
echo.
echo To stop the application at any time, press Ctrl + C in this window.
echo.

setlocal enabledelayedexpansion

REM First check if streamlit is available on standard PATH
where streamlit >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    streamlit run app.py
    goto end
)

REM Check if python is on PATH
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python -m streamlit run app.py
    goto end
)

REM Fallback directly to Python 3.11 installation directory
if exist "C:\Users\POOJITA\Python311\Scripts\streamlit.exe" (
    "C:\Users\POOJITA\Python311\Scripts\streamlit.exe" run app.py
    goto end
)

if exist "C:\Users\POOJITA\Python311\python.exe" (
    "C:\Users\POOJITA\Python311\python.exe" -m streamlit run app.py
    goto end
)

echo [ERROR] Could not find Python or Streamlit.
echo Please run: C:\Users\POOJITA\Python311\python.exe -m streamlit run app.py
pause

:end
