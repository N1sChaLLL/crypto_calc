@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
    python calculator.py
) else (
    py -3 calculator.py
)
if errorlevel 1 pause
